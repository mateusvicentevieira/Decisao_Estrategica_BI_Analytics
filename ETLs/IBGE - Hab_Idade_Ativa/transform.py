# Bibliotecas e importações:

import re

from extract import extrair_dados

# Padronizando os nomes dos municípios:

def padronizar_municipio(municipio):

    municipio = municipio.strip()

    if municipio.endswith("- SC"):
        municipio = municipio[:-5]

    return municipio.strip()


# Convertendo e tratando os valores das faixas etárias:

def tratar_valor(valor):

    # Tratar valores ausentes ou vazios:

    if valor is None:
        return 0

    if not isinstance(valor, str):
        if type(valor) is int:
            return valor if valor >= 0 else 0

        return 0

    valor = valor.strip()

    if valor in ("", "-"):
        return 0

    # Converter para inteiro:

    try:
        valor_convertido = int(valor)

    except (ValueError, TypeError):
        return 0

    # Impedir valores negativos:

    if valor_convertido < 0:
        return 0

    return valor_convertido


# Transformando e padronizando os dados:

def transformar_dados(dados):

    dados_transformados = []

    for registro in dados:

        # Verificar se o registro é um dicionário:

        if not isinstance(registro, dict):
            raise TypeError(
                f"O registro deve ser um dicionário: {registro}"
            )

        # Verificar os campos obrigatórios:

        if "id_municipio" not in registro or "municipio" not in registro:
            raise ValueError(
                f"Registro sem identificação do município: {registro}"
            )

        # Verificar os tipos dos campos de identificação:

        if not isinstance(registro["id_municipio"], str):
            raise TypeError("id_municipio deve ser str")

        if not isinstance(registro["municipio"], str):
            raise TypeError("municipio deve ser str")

        # Padronizar os campos de identificação:

        linha = {
            "id_municipio": registro["id_municipio"].strip(),
            "municipio": padronizar_municipio(
                registro["municipio"]
            )
        }

        # Identificar e tratar todas as faixas etárias:

        for campo, valor in registro.items():

            if campo.startswith("valor_"):
                linha[campo] = tratar_valor(valor)

        # Armazenar o registro transformado:

        dados_transformados.append(linha)

    return dados_transformados


# Testando a transformação quando o arquivo é executado diretamente:

if __name__ == "__main__":

    dados_extraidos = extrair_dados()

    dados_transformados = transformar_dados(dados_extraidos)

    # Relatório final:

    print(f"Registros recebidos: {len(dados_extraidos)}")
    print(f"Registros transformados: {len(dados_transformados)}")

    print("Primeiros registros transformados:")

    for registro in dados_transformados[:5]:
        print(registro)
