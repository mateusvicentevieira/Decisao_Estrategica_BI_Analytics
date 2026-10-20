# Bibliotecas e importações:

from collections import defaultdict

from extract import ANO_REFERENCIA


# Constantes:

CAMPO_VALOR = f"valor_{ANO_REFERENCIA}"


# Agrupando os dados por município e somando os valores:

def agregar_dados(dados):

    municipios_agrupados = defaultdict(int)
    nomes_municipios = {}

    for registro in dados:

        # Identificando o município:

        id_municipio = registro["id_municipio"]
        municipio = registro["municipio"]
        valor = registro[CAMPO_VALOR]

        # Somando os valores do mesmo município:

        municipios_agrupados[id_municipio] += valor

        # Armazenando o nome do município:

        nomes_municipios[id_municipio] = municipio

    # Organizando os dados agregados:

    dados_agregados = []

    for id_municipio, valor_total in municipios_agrupados.items():

        linha = {
            "id_municipio": id_municipio,
            "municipio": nomes_municipios[id_municipio],
            CAMPO_VALOR: valor_total
        }

        dados_agregados.append(linha)

    return dados_agregados


# Testando a agregação quando o arquivo é executado diretamente:

if __name__ == "__main__":

    from extract import extrair_dados
    from transform import transformar_dados
    from validate import validar_registros

    dados_extraidos = extrair_dados()

    dados_transformados = transformar_dados(dados_extraidos)

    dados_validos, dados_invalidos, duplicados = validar_registros(
        dados_transformados
    )

    dados_agregados = agregar_dados(dados_validos)

    print(f"Registros antes da agregação: {len(dados_validos)}")
    print(f"Municípios após a agregação: {len(dados_agregados)}")

    print("Primeiros registros agregados:")

    for registro in dados_agregados[:10]:
        print(registro)
