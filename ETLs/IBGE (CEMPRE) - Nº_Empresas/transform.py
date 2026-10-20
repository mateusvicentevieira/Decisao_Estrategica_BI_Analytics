# Bibliotecas e importações:

from extract import ANO_REFERENCIA, CATEGORIAS_EMPRESAS


# Constantes:

CAMPO_VALOR = f"valor_{ANO_REFERENCIA}"

CAMPOS_OBRIGATORIOS = [
    "id_municipio",
    "municipio",
    "categoria_id",
    "categoria",
    CAMPO_VALOR
]


# Padronizando os nomes dos municípios:

def padronizar_municipio(municipio):

    municipio = municipio.strip()

    if municipio.endswith(" - SC"):
        municipio = municipio[:-5]

    return municipio.strip()


# Tratando os valores numéricos:

def tratar_valor(valor):

    if valor is None or str(valor).strip() in ("", "-"):
        valor = "0"

    try:
        return int(valor)

    except (ValueError, TypeError):
        return 0


# Transformando e padronizando os dados:

def transformar_dados(dados):

    dados_transformados = []

    for registro in dados:

        # Verificando se o registro é um dicionário:

        if not isinstance(registro, dict):
            raise TypeError("O registro deve ser um dicionário")

        # Verificando os campos obrigatórios:

        if not all(
            campo in registro
            for campo in CAMPOS_OBRIGATORIOS
        ):
            raise ValueError(
                f"Registro com campos ausentes: {registro}"
            )

        # Verificando os tipos dos campos textuais:

        for campo in (
            "id_municipio",
            "municipio",
            "categoria_id",
            "categoria"
        ):

            if not isinstance(registro[campo], str):
                raise TypeError(f"{campo} deve ser str")

        # Extraindo e padronizando os campos:

        id_municipio = registro["id_municipio"].strip()

        municipio = padronizar_municipio(
            registro["municipio"]
        )

        categoria_id = registro["categoria_id"].strip()

        categoria = registro["categoria"].strip()

        valor = tratar_valor(registro[CAMPO_VALOR])

        # Organizando os dados transformados:

        linha = {
            "id_municipio": id_municipio,
            "municipio": municipio,
            "categoria_id": categoria_id,
            "categoria": categoria,
            CAMPO_VALOR: valor
        }

        # Armazenando o registro transformado:

        dados_transformados.append(linha)

    return dados_transformados


# Testando a transformação quando o arquivo é executado diretamente:

if __name__ == "__main__":

    from extract import extrair_dados

    dados_extraidos = extrair_dados()

    dados_transformados = transformar_dados(dados_extraidos)

    # Relatório final:

    print(f"Registros recebidos: {len(dados_extraidos)}")
    print(f"Registros transformados: {len(dados_transformados)}")

    print("Primeiros registros transformados:")

    for registro in dados_transformados[:10]:
        print(registro)
