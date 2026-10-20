# Bibliotecas e importações:

import re
import requests


# Constantes:

ANOS_REFERENCIA = "2022",'2010','2000','1991','1980'

URL_API_1 = (
'https://servicodados.ibge.gov.br/api/v3/agregados/10053/periodos/2022/variaveis/9599?localidades=N6[N3[42]]&classificacao=11558[46292]|14[200]'
)

URL_API_2 = (
'https://servicodados.ibge.gov.br/api/v3/agregados/206/periodos/2010/variaveis/96?localidades=N6[N3[42]]&classificacao=1[0]|65[0]'
)
URL_API_3 = (
'https://servicodados.ibge.gov.br/api/v3/agregados/206/periodos/2000/variaveis/96?localidades=N6[N3[42]]&classificacao=1[0]|65[0]'
)

URL_API_4 = (
'https://servicodados.ibge.gov.br/api/v3/agregados/206/periodos/1991/variaveis/96?localidades=N6[N3[42]]&classificacao=1[0]|65[0]'
)

URL_API_5 = (
'https://servicodados.ibge.gov.br/api/v3/agregados/206/periodos/1980/variaveis/96?localidades=N6[N3[42]]&classificacao=1[0]|65[0]'
)

# Extraindo os dados de um ano específico a partir da API do IBGE:

def extrair_dados_ano(url, ano):

    tentativas = 3

    for tentativa in range(tentativas):

        try:

            resposta = requests.get(url, timeout=60)
            resposta.raise_for_status()

            dados = resposta.json()

            # Acessando a primeira série de resultados:
            series = dados[0]["resultados"][0]["series"]
            break

        except (requests.exceptions.RequestException, TimeoutError):

            if tentativa == tentativas - 1:
                raise

            import time
            time.sleep(2)

    lista_ano = []

    for registro in series:

        id_municipio = registro["localidade"]["id"]
        municipio = registro["localidade"]["nome"]
        valor = registro["serie"].get(str(ano))

        lista_ano.append({
            "id_municipio": id_municipio,
            "municipio": municipio,
            f"valor_{ano}": valor
        })

    return lista_ano


# Funções de extração para cada ano:

def extrair_dados_2022():
    return extrair_dados_ano(URL_API_1, "2022")


def extrair_dados_2010():
    return extrair_dados_ano(URL_API_2, "2010")


def extrair_dados_2000():
    return extrair_dados_ano(URL_API_3, "2000")


def extrair_dados_1991():
    return extrair_dados_ano(URL_API_4, "1991")


def extrair_dados_1980():
    return extrair_dados_ano(URL_API_5, "1980")


# Extraindo dados de todas as APIs separadamente por variável:

def extrair_dados():

    dados_extraidos_2022 = extrair_dados_2022()
    dados_extraidos_2010 = extrair_dados_2010()
    dados_extraidos_2000 = extrair_dados_2000()
    dados_extraidos_1991 = extrair_dados_1991()
    dados_extraidos_1980 = extrair_dados_1980()

    return (
        dados_extraidos_2022,
        dados_extraidos_2010,
        dados_extraidos_2000,
        dados_extraidos_1991,
        dados_extraidos_1980
    )


# Testando a extração quando o arquivo é executado diretamente:

if __name__ == "__main__":

    (
        dados_extraidos_2022,
        dados_extraidos_2010,
        dados_extraidos_2000,
        dados_extraidos_1991,
        dados_extraidos_1980
    ) = extrair_dados()

    print(f"2022 - Municípios extraídos: {len(dados_extraidos_2022)}")
    print(f"2010 - Municípios extraídos: {len(dados_extraidos_2010)}")
    print(f"2000 - Municípios extraídos: {len(dados_extraidos_2000)}")
    print(f"1991 - Municípios extraídos: {len(dados_extraidos_1991)}")
    print(f"1980 - Municípios extraídos: {len(dados_extraidos_1980)}")

    print("\nExemplo do primeiro registro de cada ano:")
    print("2022:", dados_extraidos_2022[0])
    print("2010:", dados_extraidos_2010[0])
    print("2000:", dados_extraidos_2000[0])
    print("1991:", dados_extraidos_1991[0])
    print("1980:", dados_extraidos_1980[0])
