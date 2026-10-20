# Bibliotecas e importações:

import re

from extract import extrair_dados
from aggregate import agregar_dados


# Padronizando os nomes dos municípios:

def padronizar_municipio(municipio):

    if not isinstance(municipio, str):
        municipio = str(municipio)

    municipio = municipio.strip()

    # Retirando o sufixo '- SC' do final dos nomes:
    municipio = re.sub(r"\s*-\s*SC$", "", municipio)

    return municipio.strip()


# Convertendo e tratando os valores das colunas:

def tratar_valor(valor):

    # Tratar valores ausentes:
    if valor is None:
        return 0

    # Tratar float ou booleano:
    if isinstance(valor, (float, bool)):
        return 0

    # Tratar tipo inteiro:
    if isinstance(valor, int):
        return valor if valor >= 0 else 0

    # Tratar valores em formato string:
    if isinstance(valor, str):
        valor = valor.strip()

        # Strings vazias ou marcadores de ausência ('', '-', '...'):
        if valor in ("", "-", "...", ".."):
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
        id_municipio_original = registro.get("id_municipio")
        nome_original = registro.get("municipio") or registro.get("nome_municipio")

        if id_municipio_original is None or nome_original is None:
            raise ValueError(
                f"Registro sem identificação do município: {registro}"
            )

        municipio_padronizado = padronizar_municipio(nome_original)

        # Padronizar os campos de identificação (id_municipio garantido como str):
        linha = {
            "id_municipio": str(id_municipio_original).strip(),
            "municipio": municipio_padronizado,
            "nome_municipio": municipio_padronizado
        }

        # Identificar e tratar todas as variáveis de valores dos anos:
        for campo, valor in registro.items():
            if campo.startswith("valor_"):
                linha[campo] = tratar_valor(valor)

        # Armazenar o registro transformado:
        dados_transformados.append(linha)

    return dados_transformados


# Testando a transformação quando o arquivo é executado diretamente:

if __name__ == "__main__":

    dados_extraidos = extrair_dados()

    dados_agregados = agregar_dados(dados_extraidos)

    dados_transformados = transformar_dados(dados_agregados)

    # Relatório final:
    print(f"Registros agregados recebidos: {len(dados_agregados)}")
    print(f"Registros transformados: {len(dados_transformados)}")

    print("\nPrimeiros registros transformados:")
    for registro in dados_transformados[:5]:
        print(registro)
