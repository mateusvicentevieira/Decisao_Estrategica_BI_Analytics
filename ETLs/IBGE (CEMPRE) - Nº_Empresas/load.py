# Bibliotecas e importações:

import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv

from extract import ANO_REFERENCIA


# Carregando as variáveis de ambiente:

CAMINHO_ENV = Path(__file__).resolve().parent / ".env"

load_dotenv(dotenv_path=CAMINHO_ENV)


# Constantes:

NOME_TABELA = "empresas_construcao_municipio"

CAMPO_VALOR = f"valor_{ANO_REFERENCIA}"

CAMPOS_CARGA = [
    "id_municipio",
    "municipio",
    CAMPO_VALOR
]

CONFIG_BANCO = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}

SQL_INSERCAO = f"""
    INSERT INTO public.{NOME_TABELA}
        (id_municipio, municipio, {CAMPO_VALOR})
    VALUES (%s, %s, %s)
    ON CONFLICT (id_municipio)
    DO UPDATE SET
        municipio = EXCLUDED.municipio,
        {CAMPO_VALOR} = EXCLUDED.{CAMPO_VALOR}
"""


# Verificando as configurações do banco:

def validar_configuracao():

    campos_ausentes = [
        campo
        for campo, valor in CONFIG_BANCO.items()
        if not valor
    ]

    if campos_ausentes:
        raise ValueError(
            "Configurações ausentes: "
            + ", ".join(campos_ausentes)
        )


# Carregando os dados no PostgreSQL:

def carregar_dados(dados):

    if not dados:
        print("Nenhum registro para carregar.")
        return 0

    validar_configuracao()

    try:

        # Estabelecendo a conexão com o banco:

        with psycopg.connect(**CONFIG_BANCO) as conexao:

            # Criando o cursor para executar comandos SQL:

            with conexao.cursor() as cursor:

                # Preparando os registros para inserção:

                valores = [
                    tuple(registro[campo] for campo in CAMPOS_CARGA)
                    for registro in dados
                ]

                # Inserindo ou atualizando os registros:

                cursor.executemany(
                    SQL_INSERCAO,
                    valores
                )

                registros_carregados = len(valores)

        # Confirmando o resultado da carga:

        print("Carga realizada com sucesso.")

        return registros_carregados

    except psycopg.Error as erro:

        # Informando erros de conexão ou execução SQL:

        print(f"Erro ao carregar os dados: {erro}")

        raise


# Testando a carga quando o arquivo é executado diretamente:

if __name__ == "__main__":

    from extract import extrair_dados
    from transform import transformar_dados
    from validate import validar_registros
    from aggregate import agregar_dados

    # Extraindo os dados:

    dados_extraidos = extrair_dados()

    # Transformando os dados:

    dados_transformados = transformar_dados(dados_extraidos)

    # Validando os dados transformados:

    dados_validos, dados_invalidos, duplicados = validar_registros(
        dados_transformados
    )

    print(f"Registros inválidos: {len(dados_invalidos)}")
    print(f"Registros duplicados: {len(duplicados)}")

    # Agregando os registros por município:

    dados_agregados = agregar_dados(dados_validos)

    # Carregando os dados agregados:

    total_carregado = carregar_dados(dados_agregados)

    # Relatório final:

    print(f"Registros extraídos: {len(dados_extraidos)}")
    print(f"Registros válidos: {len(dados_validos)}")
    print(f"Municípios agregados: {len(dados_agregados)}")
    print(f"Registros carregados: {total_carregado}")
