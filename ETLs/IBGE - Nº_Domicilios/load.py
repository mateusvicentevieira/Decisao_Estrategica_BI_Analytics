# Bibliotecas e importações:

import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv


# Carregando as variáveis de ambiente:

CAMINHO_ENV = Path(__file__).resolve().parent / ".env"

load_dotenv(dotenv_path=CAMINHO_ENV)


# Constantes:

NOME_TABELA = "domicilios_municipio"

CAMPOS_CARGA = [
    "id_municipio",
    "municipio",
    "valor_2022",
    "valor_2010",
    "valor_2000",
    "valor_1991",
    "valor_1980"
]

CONFIG_BANCO = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}

SQL_CRIACAO_TABELA = """
    CREATE TABLE IF NOT EXISTS public.domicilios_municipio (
        id_municipio VARCHAR(7) PRIMARY KEY,
        municipio VARCHAR(255) NOT NULL,
        valor_2022 INTEGER NOT NULL DEFAULT 0
    );

    ALTER TABLE public.domicilios_municipio ADD COLUMN IF NOT EXISTS valor_2010 INTEGER DEFAULT 0;
    ALTER TABLE public.domicilios_municipio ADD COLUMN IF NOT EXISTS valor_2000 INTEGER DEFAULT 0;
    ALTER TABLE public.domicilios_municipio ADD COLUMN IF NOT EXISTS valor_1991 INTEGER DEFAULT 0;
    ALTER TABLE public.domicilios_municipio ADD COLUMN IF NOT EXISTS valor_1980 INTEGER DEFAULT 0;
"""

SQL_INSERCAO = """
    INSERT INTO public.domicilios_municipio
        (id_municipio, municipio, valor_2022, valor_2010, valor_2000, valor_1991, valor_1980)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (id_municipio)
    DO UPDATE SET
        municipio = EXCLUDED.municipio,
        valor_2022 = EXCLUDED.valor_2022,
        valor_2010 = EXCLUDED.valor_2010,
        valor_2000 = EXCLUDED.valor_2000,
        valor_1991 = EXCLUDED.valor_1991,
        valor_1980 = EXCLUDED.valor_1980
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

            # Criando o cursor:

            with conexao.cursor() as cursor:

                # Garantindo a existência da tabela e das colunas de todos os anos:

                cursor.execute(SQL_CRIACAO_TABELA)

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

        # A conexão confirma a transação automaticamente:

        print("Carga realizada com sucesso.")

        return registros_carregados

    except (psycopg.Error, KeyError, TypeError) as erro:

        print(f"Erro ao carregar os dados: {erro}")

        raise


# Executando o ETL completo para teste:

if __name__ == "__main__":

    from extract import extrair_dados
    from aggregate import agregar_dados
    from transform import transformar_dados
    from validate import validar_dados

    # 1. Extração:
    dados_extraidos = extrair_dados()

    # 2. Agregação:
    dados_agregados = agregar_dados(dados_extraidos)

    # 3. Transformação:
    dados_transformados = transformar_dados(dados_agregados)

    # 4. Validação:
    dados_validos, dados_invalidos = validar_dados(dados_transformados)

    print(f"Registros agregados: {len(dados_agregados)}")
    print(f"Registros válidos: {len(dados_validos)}")
    print(f"Registros inválidos: {len(dados_invalidos)}")

    # 5. Carga:
    total_carregado = carregar_dados(dados_validos)

    # Relatório final:
    print(f"Registros carregados ou atualizados: {total_carregado}")
