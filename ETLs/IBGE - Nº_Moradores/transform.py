# Bibliotecas e importações:

from validate import CAMPOS_OBRIGATORIOS


# Padronizando os nomes dos municípios:

def padronizar_municipio(municipio):

    municipio = municipio.strip()

    if municipio.endswith(" - SC"):
        municipio = municipio[:-5]

    return municipio.strip()


# Transformando e padronizando os dados:

def transformar_dados(dados):

    dados_transformados = []

    for registro in dados:

        # Verificar se o registro possui os campos obrigatórios:

        if not all(
            campo in registro
            for campo in CAMPOS_OBRIGATORIOS
        ):
            raise ValueError(
                f"Registro com campos ausentes: {registro}"
            )

        # Verificar os tipos de dados antes da transformação:

        if not isinstance(registro["id_municipio"], str):
            raise TypeError("id_municipio deve ser str")

        if not isinstance(registro["municipio"], str):
            raise TypeError("municipio deve ser str")

        if type(registro["valor_2022"]) is not int:
            raise TypeError("valor_2022 deve ser int")

        # Extraindo e padronizando os campos:

        id_municipio = registro["id_municipio"].strip()

        municipio = padronizar_municipio(
            registro["municipio"]
        )

        valor_2022 = registro["valor_2022"]

        # Organizando os dados para o carregamento:

        linha = {
            "id_municipio": id_municipio,
            "municipio": municipio,
            "valor_2022": valor_2022
        }

        # Armazenando o registro transformado:

        dados_transformados.append(linha)

    return dados_transformados


# Testando a transformação quando o arquivo é executado diretamente:

if __name__ == "__main__":

    from extract import extrair_dados
    from validate import validar_registros, exibir_relatorio

    dados_extraidos = extrair_dados()

    dados_validos, dados_invalidos, duplicados = validar_registros(
        dados_extraidos
    )

    exibir_relatorio(
        dados_extraidos,
        dados_validos,
        dados_invalidos,
        duplicados
    )

    dados_transformados = transformar_dados(dados_validos)

    # Relatório final:

    print(f"Registros recebidos: {len(dados_validos)}")
    print(f"Registros transformados: {len(dados_transformados)}")