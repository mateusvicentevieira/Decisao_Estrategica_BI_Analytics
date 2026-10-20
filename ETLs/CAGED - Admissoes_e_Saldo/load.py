# Bibliotecas e importações:

import os
import re
from pathlib import Path
from typing import Any

import psycopg
from dotenv import load_dotenv


# Carregando as variáveis de ambiente:

CAMINHO_ENV = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=CAMINHO_ENV)


# Constantes:

NOME_TABELA = "caged_municipio"

CAMPOS_IDENTIFICACAO = [
    "id_municipio",
    "municipio",
]

PREFIXOS_KPI = (
    "admissoes_",
    "saldo_",
)

CONFIG_BANCO = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}


# Verificando as configurações do banco:

def validar_configuracao():
    """Confere se as variáveis obrigatórias de conexão estão preenchidas."""

    campos_ausentes = [
        campo
        for campo, valor in CONFIG_BANCO.items()
        if not valor
    ]

    if campos_ausentes:
        raise ValueError(
            "Configurações ausentes no arquivo .env: "
            + ", ".join(campos_ausentes)
        )


# Identificando os indicadores mensais:

def identificar_campos_kpi(dados):
    """Retorna os campos mensais presentes nos registros."""

    campos_kpi = set()

    for registro in dados:
        if not isinstance(registro, dict):
            continue

        for campo in registro:
            if (
                isinstance(campo, str)
                and campo.startswith(PREFIXOS_KPI)
            ):
                campos_kpi.add(campo)

    return sorted(campos_kpi)


# Validando a estrutura dos registros para carga:

def validar_registros_carga(dados, campos_kpi):
    """Valida registros agregados antes de enviar ao PostgreSQL."""

    if not isinstance(dados, (list, tuple)):
        raise TypeError("Os dados para carga devem ser uma lista ou tupla.")

    if not dados:
        return

    if not campos_kpi:
        raise ValueError("Nenhum campo mensal do CAGED foi encontrado.")

    ids_municipios = []

    for indice, registro in enumerate(dados):

        if not isinstance(registro, dict):
            raise TypeError(
                f"Registro {indice} não é um dicionário."
            )

        campos_ausentes = [
            campo
            for campo in CAMPOS_IDENTIFICACAO
            if campo not in registro
        ]

        if campos_ausentes:
            raise ValueError(
                f"Registro {indice} sem os campos obrigatórios: "
                + ", ".join(campos_ausentes)
            )

        id_municipio = registro["id_municipio"]
        municipio = registro["municipio"]

        if not isinstance(id_municipio, str):
            raise TypeError(
                f"Registro {indice}: id_municipio deve ser str."
            )

        if not id_municipio.isdigit() or len(id_municipio) != 7:
            raise ValueError(
                f"Registro {indice}: código IBGE inválido."
            )

        if not isinstance(municipio, str) or not municipio.strip():
            raise ValueError(
                f"Registro {indice}: município vazio ou inválido."
            )

        ids_municipios.append(id_municipio)

        campos_presentes = {
            campo
            for campo in registro
            if isinstance(campo, str)
            and campo.startswith(PREFIXOS_KPI)
        }

        campos_ausentes = set(campos_kpi) - campos_presentes
        campos_extras = campos_presentes - set(campos_kpi)

        if campos_ausentes:
            raise ValueError(
                f"Registro {indice} sem indicadores: "
                + ", ".join(sorted(campos_ausentes))
            )

        if campos_extras:
            raise ValueError(
                f"Registro {indice} contém indicadores inesperados: "
                + ", ".join(sorted(campos_extras))
            )

        for campo in campos_kpi:
            valor = registro[campo]

            if type(valor) is not int:
                raise TypeError(
                    f"Registro {indice}: {campo} deve ser int."
                )

            if campo.startswith("admissoes_") and valor < 0:
                raise ValueError(
                    f"Registro {indice}: {campo} não pode ser negativo."
                )

            # O saldo pode ser negativo; por isso, não o rejeitamos.

    if len(ids_municipios) != len(set(ids_municipios)):
        raise ValueError(
            "Existem municípios duplicados nos dados de carga."
        )


# Criando a tabela de destino:

def criar_tabela(cursor, campos_kpi):
    """Cria a tabela com uma coluna para cada indicador mensal."""

    colunas = [
        '"id_municipio" VARCHAR(7) PRIMARY KEY',
        '"municipio" VARCHAR(100) NOT NULL',
    ]

    for campo in campos_kpi:
        # Só aceita nomes no formato admissoes_YYYYMM ou saldo_YYYYMM.
        if not re.fullmatch(r"(admissoes|saldo)_\d{6}", campo):
            raise ValueError(f"Nome de coluna mensal inválido: {campo}")

        colunas.append(f'"{campo}" INTEGER NOT NULL')

    sql = (
        f'CREATE TABLE IF NOT EXISTS public.{NOME_TABELA} ('
        + ", ".join(colunas)
        + ")"
    )

    cursor.execute(sql)

    # Se a tabela já existia, adiciona as colunas dos novos meses.
    for campo in campos_kpi:
        cursor.execute(
            f'ALTER TABLE public.{NOME_TABELA} '
            f'ADD COLUMN IF NOT EXISTS "{campo}" INTEGER NOT NULL DEFAULT 0'
        )


# Carregando os dados no PostgreSQL:

def carregar_dados(dados, tamanho_lote=500):
    """Insere ou atualiza registros agregados do Novo CAGED."""

    if not dados:
        print("Nenhum registro para carregar.")
        return 0

    if tamanho_lote <= 0:
        raise ValueError("O tamanho do lote deve ser maior que zero.")

    validar_configuracao()

    campos_kpi = identificar_campos_kpi(dados)
    validar_registros_carga(dados, campos_kpi)

    campos_carga = CAMPOS_IDENTIFICACAO + campos_kpi
    colunas_sql = ", ".join(f'"{campo}"' for campo in campos_carga)
    placeholders = ", ".join(["%s"] * len(campos_carga))

    campos_atualizacao = [
        campo for campo in campos_carga
        if campo != "id_municipio"
    ]

    atualizacao_sql = ", ".join(
        f'"{campo}" = EXCLUDED."{campo}"'
        for campo in campos_atualizacao
    )

    sql_insercao = f"""
        INSERT INTO public.{NOME_TABELA} ({colunas_sql})
        VALUES ({placeholders})
        ON CONFLICT ("id_municipio")
        DO UPDATE SET {atualizacao_sql}
    """

    valores = [
        tuple(registro[campo] for campo in campos_carga)
        for registro in dados
    ]

    with psycopg.connect(**CONFIG_BANCO) as conexao:
        with conexao.cursor() as cursor:
            criar_tabela(cursor, campos_kpi)

            for inicio in range(0, len(valores), tamanho_lote):
                lote = valores[inicio:inicio + tamanho_lote]
                cursor.executemany(sql_insercao, lote)

    print(f"Carga realizada com sucesso: {len(valores)} municípios.")
    return len(valores)


# Testando a carga quando o arquivo é executado diretamente:

if __name__ == "__main__":
    print(
        "Para testar a carga, execute a pipeline pelo main.py. "
        "Isso garante que extract, transform, aggregate e validate "
        "sejam executados na ordem correta."
    )
