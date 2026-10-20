# Bibliotecas e importações:

import re

from extract import extrair_dados

# Padronizando os nomes dos municípios:

def padronizar_municipio(municipio):

    if not isinstance(municipio, str):
        municipio = str(municipio)

    municipio = municipio.strip()

    # Retirando o sufixo '- SC' do final dos nomes:
    municipio = re.sub(r"\s*-\s*SC$", "", municipio)

    return municipio.strip()


# Convertendo e tratando os valores das faixas etárias:

def tratar_valor(valor):

    # Tratar valores ausentes:
    if valor is None:
        return 0

    # Tratar tipo float ou booleano:
    if isinstance(valor, (float, bool)):
        return 0

    # Tratar tipo inteiro:
    if isinstance(valor, int):
        return valor if valor >= 0 else 0

    # Tratar valores em string:
    if isinstance(valor, str):
        valor = valor.strip()

        # Strings vazias ou marcadores de ausência:
        if valor in ("", "-"):
            return 0

        # Se for string representando float (ex: '12.5' ou '12,5'):
        if "." in valor or "," in valor:
            return 0

        # Tentar converter para inteiro:
        try:
            valor_convertido = int(valor)
        except (ValueError, TypeError):
            return 0

        # Impedir valores negativos:
        if valor_convertido < 0:
            return 0

        return valor_convertido

    return 0


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

        if registro["id_municipio"] is None or registro["municipio"] is None:
            raise ValueError(
                f"Registro com identificação nula: {registro}"
            )

        # Padronizar os campos de identificação (id_municipio garantido como str):
        linha = {
            "id_municipio": str(registro["id_municipio"]).strip(),
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
