# Bibliotecas e importações:

import requests as re


# Constantes:

ANO_REFERENCIA = "2022"

URL_API = (
'https://servicodados.ibge.gov.br/api/v3/agregados/10289/periodos/2022/variaveis/13537?localidades=N6[N3[42]]&classificacao=2[6794]|86[95251]'
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

    # Extraindo os campos necessários:

    dados_extraidos = []

    for registro in series:

        # Extraindo os campos:

        id_municipio = registro["localidade"]["id"]
        municipio = registro["localidade"]["nome"]
        valor = registro["serie"].get(ANO_REFERENCIA)

        # Organizando os campos em um dicionário:

        linha = {
            "id_municipio": id_municipio,
            "municipio": municipio,
            f"valor_{ANO_REFERENCIA}": valor
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
