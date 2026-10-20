# Bibliotecas e importações:

import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv

from extract import extrair_dados
from validate import validar_registros, exibir_relatorio
from transform import transformar_dados


# Carregando as variáveis de ambiente:

CAMINHO_ENV = Path(__file__).resolve().parent / ".env"

load_dotenv(CAMINHO_ENV)


# Constantes:

CONFIG_BANCO = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}

NOME_TABELA = "rendimento_mediano_municipio"


# Carregando os dados no PostgreSQL:

def carregar_dados(dados):

    # Verificar se existem dados para carregar:

    if not dados:
        print("Nenhum dado disponível para carregar.")
        return

    # Comando SQL para inserir ou atualizar os registros:

    comando_sql = f"""
        INSERT INTO {NOME_TABELA} (
            id_municipio,
            municipio,
            valor_2022
        )
        VALUES (%s, %s, %s)
        ON CONFLICT (id_municipio)
        DO UPDATE SET
            municipio = EXCLUDED.municipio,
            valor_2022 = EXCLUDED.valor_2022;
    """

    # Preparar os dados para inserção:

    valores = [
        (
            registro["id_municipio"],
            registro["municipio"],
            registro["valor_2022"]
        )
        for registro in dados
    ]

    # Conectar ao banco e carregar os dados:

    with psycopg.connect(**CONFIG_BANCO) as conexao:

        with conexao.cursor() as cursor:

            cursor.executemany(comando_sql, valores)

    print(f"Registros processados: {len(valores)}")
    print("Carga concluída com sucesso!")


# Executando o ETL completo:

if __name__ == "__main__":

    # Extração:

    dados_extraidos = extrair_dados()

    print(f"Registros extraídos: {len(dados_extraidos)}")

    # Validação:

    dados_validos, dados_invalidos, duplicados = validar_registros(
        dados_extraidos
    )

    exibir_relatorio(
        dados_extraidos,
        dados_validos,
        dados_invalidos,
        duplicados
    )

    # Transformação:

    dados_transformados = transformar_dados(dados_validos)

    print(f"Registros transformados: {len(dados_transformados)}")

    # Carga:

    carregar_dados(dados_transformados)
