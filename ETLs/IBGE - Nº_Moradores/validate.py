# Bibliotecas e importações:

from extract import extrair_dados


# Constantes:

CAMPOS_OBRIGATORIOS = [
    "id_municipio",
    "municipio",
    "valor_2022"
]

TIPOS_ESPERADOS = {
    "id_municipio": str,
    "municipio": str,
    "valor_2022": int
}

CHAVE_UNICA = ["id_municipio"]


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

        # Verificar campos obrigatórios:

        for campo in campos_obrigatorios:

            if campo not in registro:
                erros.append(f"Campo ausente: {campo}")

            elif valor_vazio(registro[campo]):
                erros.append(f"Campo vazio: {campo}")

        # Verificar tipos de dados:

        for campo, tipo_esperado in tipos_esperados.items():

            if campo not in registro or valor_vazio(registro[campo]):
                continue

            if type(registro[campo]) is not tipo_esperado:
                erros.append(f"Tipo inválido: {campo}")

        # Verificar valores negativos:

        valor = registro.get("valor_2022")

        if type(valor) in (int, float) and valor < 0:
            erros.append("Valor negativo: valor_2022")

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

    # Validar campos obrigatórios, tipos e valores:

    validos, invalidos = validar_dados(
        dados,
        CAMPOS_OBRIGATORIOS,
        TIPOS_ESPERADOS
    )

    # Identificar registros duplicados:

    duplicados = validar_unicidade(
        dados,
        CHAVE_UNICA
    )

    # Identificar as chaves duplicadas:

    chaves_duplicadas = {
        tuple(registro[campo] for campo in CHAVE_UNICA)
        for registro in duplicados
    }

    # Remover registros com chaves duplicadas dos dados válidos:

    validos_filtrados = []

    for registro in validos:

        chave = tuple(
            registro[campo] for campo in CHAVE_UNICA
        )

        if chave in chaves_duplicadas:

            invalidos.append({
                "registro": registro,
                "erros": ["ID municipal duplicado"]
            })

        else:
            validos_filtrados.append(registro)

    return validos_filtrados, invalidos, duplicados


# Exibindo o relatório das validações:

def exibir_relatorio(dados, validos, invalidos, duplicados):

    if duplicados:
        print(f"Erro: {len(duplicados)} registro(s) duplicado(s).")
    else:
        print("Nenhum dado duplicado.")

    print(f"Total de registros: {len(dados)}")
    print(f"Registros válidos: {len(validos)}")
    print(f"Registros inválidos: {len(invalidos)}")

    for item in invalidos:
        print("Registro:", item["registro"])
        print("Problemas:", item["erros"])

    for registro in duplicados:
        print("Registro duplicado:", registro)


# Testando a validação quando o arquivo é executado diretamente:

if __name__ == "__main__":

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