# Bibliotecas e importações:

import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv


# Carregando as variáveis de ambiente:

CAMINHO_ENV = Path(__file__).resolve().parent / ".env"

load_dotenv(dotenv_path=CAMINHO_ENV)


# Constantes:

NOME_TABELA = "populacao_idade_municipio"

CAMPOS_CARGA = [
    "id_municipio",
    "municipio",
    "valor_total"
]

CONFIG_BANCO = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}

SQL_CRIACAO_TABELA = """
    CREATE TABLE IF NOT EXISTS public.populacao_dependente_municipio (
        id_municipio VARCHAR(7) PRIMARY KEY,
        municipio VARCHAR(255) NOT NULL,
        valor_total INTEGER NOT NULL
    );
"""

SQL_INSERCAO = """
    INSERT INTO public.populacao_dependente_municipio
        (id_municipio, municipio, valor_total)
    VALUES (%s, %s, %s)
    ON CONFLICT (id_municipio)
    DO UPDATE SET
        municipio = EXCLUDED.municipio,
        valor_total = EXCLUDED.valor_total
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

                # Garantindo que a tabela exista no banco:

                cursor.execute(SQL_CRIACAO_TABELA)

                # Preparando os registros para inserção:

                valores = [
                    (
                        registro["id_municipio"],
                        registro["municipio"],
                        registro.get("valor_total", registro.get("soma_total", 0))
                    )
                    for registro in dados
                ]

                # Inserindo ou atualizando os registros:

                cursor.executemany(
                    SQL_INSERCAO,
                    valores
                )

                registros_carregados = len(valores)

        # A conexão confirma a transação se não houver erros:

        print("Carga realizada com sucesso.")

        return registros_carregados

    except (psycopg.Error, KeyError, TypeError) as erro:

        print(f"Erro ao carregar os dados: {erro}")

        raise


# Executando o ETL completo para teste:

if __name__ == "__main__":

    from extract import extrair_dados
    from transform import transformar_dados
    from validate import validar_dados
    from aggregate import agregar_dados

    # Extraindo os dados:

    dados_extraidos = extrair_dados()

    # Transformando os dados:

    dados_transformados = transformar_dados(
        dados_extraidos
    )

    # Validando os dados:

    dados_validos, dados_invalidos = validar_dados(
        dados_transformados
    )

    print(f"Registros extraídos: {len(dados_extraidos)}")
    print(f"Registros válidos: {len(dados_validos)}")
    print(f"Registros inválidos: {len(dados_invalidos)}")

    # Agregando os dados válidos:

    dados_agregados = agregar_dados(dados_validos)

    # Carregando os dados no PostgreSQL:

    total_carregado = carregar_dados(dados_agregados)

    # Relatório final:

    print(f"Registros agregados: {len(dados_agregados)}")
    print(f"Registros carregados ou atualizados: {total_carregado}")
