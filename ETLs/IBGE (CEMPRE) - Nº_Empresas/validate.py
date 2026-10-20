# Bibliotecas e importações:

from extract import (
    ANO_REFERENCIA,
    CATEGORIAS_EMPRESAS,
    extrair_dados
)

from transform import transformar_dados


# Constantes:

CAMPO_VALOR = f"valor_{ANO_REFERENCIA}"

CAMPOS_OBRIGATORIOS = [
    "id_municipio",
    "municipio",
    "categoria_id",
    "categoria",
    CAMPO_VALOR
]

TIPOS_ESPERADOS = {
    "id_municipio": str,
    "municipio": str,
    "categoria_id": str,
    "categoria": str,
    CAMPO_VALOR: int
}

CHAVE_UNICA = ["id_municipio", "categoria_id"]


# Verificando se um valor está vazio:

def valor_vazio(valor):

    return (
        valor is None
        or (isinstance(valor, str) and valor.strip() == "")
    )


# Verificando se os dados são únicos:

def validar_unicidade(dados, campos_chave):

    chaves_encontradas = set()
    duplicados = []

    for registro in dados:

        if not isinstance(registro, dict):
            continue

        if not all(
            campo in registro and not valor_vazio(registro[campo])
            for campo in campos_chave
        ):
            continue

        chave = tuple(
            registro[campo] for campo in campos_chave
        )

        if chave in chaves_encontradas:
            duplicados.append(registro)
        else:
            chaves_encontradas.add(chave)

    return duplicados


# Verificando campos obrigatórios,
# tipos de dados e valores negativos:

def validar_dados(dados, campos_obrigatorios, tipos_esperados):

    validos = []
    invalidos = []

    for registro in dados:

        erros = []

        if not isinstance(registro, dict):
            invalidos.append({
                "registro": registro,
                "erros": ["Registro não é um dicionário"]
            })
            continue

        # Verificando campos obrigatórios:

        for campo in campos_obrigatorios:

            if campo not in registro:
                erros.append(f"Campo ausente: {campo}")

            elif valor_vazio(registro[campo]):
                erros.append(f"Campo vazio: {campo}")

        # Verificando tipos de dados:

        for campo, tipo_esperado in tipos_esperados.items():

            if campo not in registro or valor_vazio(registro[campo]):
                continue

            if type(registro[campo]) is not tipo_esperado:
                erros.append(f"Tipo inválido: {campo}")

        # Verificando categorias não esperadas:

        categoria_id = registro.get("categoria_id")

        if (
            not valor_vazio(categoria_id)
            and categoria_id not in CATEGORIAS_EMPRESAS
        ):
            erros.append("Categoria não reconhecida")

        # Verificando valores negativos:

        valor = registro.get(CAMPO_VALOR)

        if type(valor) in (int, float) and valor < 0:
            erros.append(f"Valor negativo: {CAMPO_VALOR}")

        # Separando registros válidos e inválidos:

        if erros:
            invalidos.append({
                "registro": registro,
                "erros": erros
            })
        else:
            validos.append(registro)

    return validos, invalidos


# Executando todas as validações:

def validar_registros(dados):

    # Validando campos, tipos e valores:

    validos, invalidos = validar_dados(
        dados,
        CAMPOS_OBRIGATORIOS,
        TIPOS_ESPERADOS
    )

    # Identificando registros duplicados:

    duplicados = validar_unicidade(
        dados,
        CHAVE_UNICA
    )

    # Identificando as chaves duplicadas:

    chaves_duplicadas = {
        tuple(registro[campo] for campo in CHAVE_UNICA)
        for registro in duplicados
    }

    # Removendo dos válidos todos os registros
    # que pertencem a uma chave duplicada:

    validos_filtrados = []

    for registro in validos:

        chave = tuple(
            registro[campo] for campo in CHAVE_UNICA
        )

        if chave in chaves_duplicadas:
            invalidos.append({
                "registro": registro,
                "erros": ["Combinação de município e categoria duplicada"]
            })
        else:
            validos_filtrados.append(registro)

    return validos_filtrados, invalidos, duplicados


# Exibindo o relatório das validações:

def exibir_relatorio(dados, validos, invalidos, duplicados):

    print(f"Total de registros: {len(dados)}")
    print(f"Registros válidos: {len(validos)}")
    print(f"Registros inválidos: {len(invalidos)}")
    print(f"Registros duplicados identificados: {len(duplicados)}")

    if duplicados:
        print("\nRegistros duplicados:")

        for registro in duplicados:
            print(registro)
    else:
        print("\nNenhum registro duplicado.")

    if invalidos:
        print("\nRegistros inválidos:")

        for item in invalidos:
            print("Registro:", item["registro"])
            print("Problemas:", item["erros"])


# Testando a validação quando o arquivo é executado diretamente:

if __name__ == "__main__":

    # Extraindo os dados:

    dados_extraidos = extrair_dados()

    # Transformando os dados antes da validação:

    dados_transformados = transformar_dados(dados_extraidos)

    # Validando os dados transformados:

    dados_validos, dados_invalidos, duplicados = validar_registros(
        dados_transformados
    )

    # Exibindo o relatório:

    exibir_relatorio(
        dados_transformados,
        dados_validos,
        dados_invalidos,
        duplicados
    )
