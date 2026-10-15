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
    "valor_2022"
]

CONFIG_BANCO = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}

SQL_INSERCAO = """
    INSERT INTO public.domicilios_municipio
        (id_municipio, municipio, valor_2022)
    VALUES (%s, %s, %s)
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

                # Inserindo os registros no banco:

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
    from validate import validar_registros, exibir_relatorio
    from transform import transformar_dados

    # Extraindo os dados:

    dados_extraidos = extrair_dados()

    # Validando os dados:

    dados_validos, dados_invalidos, duplicados = validar_registros(
        dados_extraidos
    )

    exibir_relatorio(
        dados_extraidos,
        dados_validos,
        dados_invalidos,
        duplicados
    )

    # Transformando os dados:

    dados_transformados = transformar_dados(dados_validos)

    # Carregando os dados:

    total_carregado = carregar_dados(dados_transformados)

    # Relatório final:

    print(f"Registros recebidos: {len(dados_transformados)}")
    print(f"Registros carregados: {total_carregado}")
