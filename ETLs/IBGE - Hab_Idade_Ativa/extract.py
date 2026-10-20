# Bibliotecas e importações:

import re
import requests


# Constantes:

ANO_REFERENCIA = "2022"

URL_API = (
    "https://servicodados.ibge.gov.br/api/v3/agregados/"
    "6893/periodos/2022/variaveis/382"
    "?localidades=N6[N3[42]]"
    "&classificacao=125[2932]|58[1143,1144,1145,1146,"
    "1147,1148,1149,1150,1151,1152,1153]|86[95251]"
)


# Identificando o campo correspondente à faixa etária:

def identificar_faixa_etaria(classificacoes):

    for classificacao in classificacoes:

        if classificacao["id"] == "58":

            categoria = classificacao["categoria"]

            # Obtendo a descrição da faixa etária:

            if isinstance(categoria, dict):
                faixa = next(iter(categoria.values()))
            else:
                faixa = categoria

            # Extraindo os limites da faixa etária:

            numeros = re.findall(r"\d+", faixa)

            if len(numeros) >= 2:
                return f"valor_{numeros[0]}a{numeros[1]}"

            # Caso a categoria não seja uma faixa numérica:

            return "valor_" + re.sub(
                r"\W+", "_", faixa.lower()
            ).strip("_")

    raise ValueError("Classificação de faixa etária não encontrada.")


# Extraindo e organizando os dados da API:

def extrair_dados():

    # Consultando a API:

    resposta = requests.get(URL_API, timeout=30)

    resposta.raise_for_status()

    dados = resposta.json()

    # Acessando os blocos de resultados:

    resultados = dados[0]["resultados"]

    # Organizando os dados por município:

    municipios = {}

    for resultado in resultados:

        # Identificando a faixa etária do bloco:

        classificacoes = resultado["classificacoes"]

        faixa_etaria = None

        for classificacao in classificacoes:

            if classificacao["id"] == "58":

                categoria = classificacao["categoria"]

                descricao = next(iter(categoria.values()))

                numeros = re.findall(r"\d+", descricao)

                if len(numeros) >= 2:

                    faixa_etaria = (
                        f"valor_{numeros[0]}a{numeros[1]}"
                    )

                else:

                    raise ValueError(
                        f"Faixa etária não reconhecida: {descricao}"
                    )

                break

        if faixa_etaria is None:

            raise ValueError(
                "Classificação de grupo de idade não encontrada."
            )

        # Acessando as séries do bloco:

        series = resultado["series"]

        for registro in series:

            # Extraindo os campos necessários:

            id_municipio = registro["localidade"]["id"]
            municipio = registro["localidade"]["nome"]

            valor_2022 = registro["serie"].get(ANO_REFERENCIA)

            # Criando o município apenas uma vez:

            if id_municipio not in municipios:

                municipios[id_municipio] = {
                    "id_municipio": id_municipio,
                    "municipio": municipio
                }

            # Armazenando o valor na coluna da faixa etária:

            municipios[id_municipio][faixa_etaria] = valor_2022

    # Convertendo o dicionário de municípios em uma lista:

    dados_extraidos = list(municipios.values())

    return dados_extraidos



# Testando a extração quando o arquivo é executado diretamente:

if __name__ == "__main__":

    dados_extraidos = extrair_dados()

    print(f"Municípios extraídos: {len(dados_extraidos)}")

    print("Primeiros registros:")

    for registro in dados_extraidos[:10]:
        print(registro)
