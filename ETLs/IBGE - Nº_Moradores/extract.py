# Bibliotecas e importações:

import requests as re


# Constantes:

URL_API = (
    "https://servicodados.ibge.gov.br/api/v3/agregados/"
    "6750/periodos/2022/variaveis/9598"
    "?localidades=N6[N3[42]]"
    "&classificacao=2[6794]|86[95251]|14[200]"
)


# Extraindo e organizando os dados da API:

def extrair_dados():

    # Consultando a API:

    resposta = re.get(URL_API, timeout=30)

    resposta.raise_for_status()

    dados = resposta.json()

    # Acessando os registros da API:

    resultados = dados[0]["resultados"]

    series = resultados[0]["series"]

    # Transformando e organizando os dados:

    dados_tratados = []

    for registro in series:

        # Extraindo os campos necessários:

        id_municipio = registro["localidade"]["id"]
        municipio = registro["localidade"]["nome"]
        valor_2022 = registro["serie"]["2022"]

        # Organizando os campos em um dicionário:

        linha = {
            "id_municipio": id_municipio,
            "municipio": municipio,
            "valor_2022": int(valor_2022)
        }

        # Armazenando o registro tratado:

        dados_tratados.append(linha)

    return dados_tratados


# Testando a extração quando o arquivo é executado diretamente:

if __name__ == "__main__":

    dados_extraidos = extrair_dados()

    print(f"Registros extraídos: {len(dados_extraidos)}")