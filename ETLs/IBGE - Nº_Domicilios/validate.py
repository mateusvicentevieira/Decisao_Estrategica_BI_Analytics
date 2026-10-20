# Bibliotecas e importações:

from collections import Counter
from extract import extrair_dados
from aggregate import agregar_dados
from transform import transformar_dados

# Constantes:

CAMPOS_OBRIGATORIOS = [
    "id_municipio",
    "municipio"
]

ANOS_ESPERADOS = [
    "2022",
    "2010",
    "2000",
    "1991",
    "1980"
]

CAMPOS_VALORES_ESPERADOS = [f"valor_{ano}" for ano in ANOS_ESPERADOS]
PREFIXO_VALORES = "valor_"


# Validando os dados:

def validar_dados(dados):

    dados_validos = []
    dados_invalidos = []

    if not isinstance(dados, list):
        raise TypeError("Os dados devem ser uma lista de registros.")

    if not dados:
        raise ValueError("A lista de dados está vazia.")

    # Contando as ocorrências de cada ID:

    ids = [
        registro.get("id_municipio")
        for registro in dados
        if isinstance(registro, dict)
    ]

    contagem_ids = Counter(ids)

    # Validando cada registro:

    for registro in dados:

        erros = []

        if not isinstance(registro, dict):
            dados_invalidos.append({
                "registro": registro,
                "erros": ["O registro não é um dicionário."]
            })
            continue

        # Verificando os campos obrigatórios:

        for campo in CAMPOS_OBRIGATORIOS:

            if campo not in registro:
                erros.append(
                    f"Campo obrigatório ausente: {campo}."
                )

            elif registro[campo] is None:
                erros.append(
                    f"O campo {campo} está vazio."
                )

            elif (
                isinstance(registro[campo], str)
                and not registro[campo].strip()
            ):
                erros.append(
                    f"O campo {campo} está vazio."
                )

        # Validando o ID do município:

        id_municipio = registro.get("id_municipio")

        if isinstance(id_municipio, str):

            if id_municipio != id_municipio.strip():
                erros.append(
                    "O ID possui espaços extras."
                )

            if not id_municipio.isdigit() or len(id_municipio) != 7:
                erros.append(
                    "O ID deve ser um código IBGE de 7 dígitos."
                )

        else:
            erros.append(
                "O ID do município deve ser str."
            )

        # Validando o nome do município:

        municipio = registro.get("municipio")

        if isinstance(municipio, str):

            if municipio != municipio.strip():
                erros.append(
                    "O nome do município possui espaços extras."
                )

            if municipio.endswith("- SC") or municipio.endswith("-SC"):
                erros.append(
                    "O nome ainda contém o sufixo '- SC'."
                )

        else:
            erros.append(
                "O nome do município deve ser str."
            )

        # Validando a presença e integridade de todos os valores de anos esperados:

        for campo in CAMPOS_VALORES_ESPERADOS:

            if campo not in registro:
                erros.append(
                    f"Campo de valor ausente: {campo}."
                )
                continue

            valor = registro[campo]

            if type(valor) is not int:
                erros.append(
                    f"{campo} deve ser int; "
                    f"recebido: {type(valor).__name__}."
                )

            elif valor < 0:
                erros.append(
                    f"{campo} não pode ter valor negativo."
                )

        # Verificando IDs duplicados:

        if (
            isinstance(id_municipio, str)
            and contagem_ids[id_municipio] > 1
        ):
            erros.append(
                f"ID de município duplicado: {id_municipio}."
            )

        # Separando os registros:

        if erros:
            dados_invalidos.append({
                "registro": registro,
                "erros": erros
            })
        else:
            dados_validos.append(registro)

    return dados_validos, dados_invalidos


# Testando a validação:

if __name__ == "__main__":

    dados_extraidos = extrair_dados()

    dados_agregados = agregar_dados(
        dados_extraidos
    )

    dados_transformados = transformar_dados(
        dados_agregados
    )

    dados_validos, dados_invalidos = validar_dados(
        dados_transformados
    )

    print(f"Registros recebidos: {len(dados_transformados)}")
    print(f"Registros válidos: {len(dados_validos)}")
    print(f"Registros inválidos: {len(dados_invalidos)}")

    if dados_invalidos:
        print("\nPrimeiros registros inválidos:")
        for item in dados_invalidos[:5]:
            print(item)
