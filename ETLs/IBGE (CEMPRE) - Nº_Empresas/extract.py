# Bibliotecas e importações:

import requests as re


# Constantes:

ANO_REFERENCIA = "2021"

CATEGORIAS_EMPRESAS = [
    "117329",
    "117330",
    "117419",
    "117420",
    "117421",
    "117422",
    "117423",
    "117424",
    "117452",
    "117453",
    "117454",
    "117455",
    "117456"
]

URL_API = (
    "https://servicodados.ibge.gov.br/api/v3/agregados/"
    "6450/periodos/2021/variaveis/706"
    "?localidades=N6[N3[42]]"
    "&classificacao=12762["
    + ",".join(CATEGORIAS_EMPRESAS)
    + "]"
)


# Extraindo e organizando os dados da API:

def extrair_dados():

    # Consultando a API:

    resposta = re.get(URL_API, timeout=30)

    resposta.raise_for_status()

    dados = resposta.json()

    # Acessando os resultados da API:

    resultados = dados[0]["resultados"]

    # Extraindo os registros de cada categoria:

    dados_extraidos = []

    for resultado in resultados:

        # Identificando a categoria:

        classificacao = resultado["classificacoes"][0]

        categoria_id, categoria_nome = next(
            iter(classificacao["categoria"].items())
        )

        # Acessando as séries dos municípios:

        series = resultado["series"]

        for registro in series:

            # Extraindo os campos necessários:

            id_municipio = registro["localidade"]["id"]
            municipio = registro["localidade"]["nome"]
            valor_2021 = registro["serie"].get(ANO_REFERENCIA)

            # Organizando os campos em um dicionário:

            linha = {
                "id_municipio": id_municipio,
                "municipio": municipio,
                "categoria_id": categoria_id,
                "categoria": categoria_nome,
                "valor_2021": valor_2021
            }

            # Armazenando o registro extraído:

            dados_extraidos.append(linha)

    return dados_extraidos


# Testando a extração quando o arquivo é executado diretamente:

if __name__ == "__main__":

    dados_extraidos = extrair_dados()

    print(f"Registros extraídos: {len(dados_extraidos)}")

    print("Primeiros registros:")

    for registro in dados_extraidos[:10]:
        print(registro)
