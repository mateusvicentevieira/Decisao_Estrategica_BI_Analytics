
# Bibliotecas e importações:

from collections import Counter
from typing import Any, Dict, List, Tuple


# Constantes:

CAMPOS_OBRIGATORIOS = [
    "id_municipio",
    "municipio",
]

PREFIXOS_KPI = (
    "admissoes_",
    "saldo_",
)


# Funções auxiliares:

def identificar_campos_kpi(registro: Dict[str, Any]) -> set:
    """Identifica os campos de indicadores mensais do CAGED."""

    return {
        campo
        for campo in registro
        if isinstance(campo, str)
        and campo.startswith(PREFIXOS_KPI)
    }


# Validando os dados:

def validar_dados(
    dados: List[Dict[str, Any]]
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Valida os registros agregados do Novo CAGED.

    Retorna:
    - dados_validos: registros aprovados;
    - dados_invalidos: registros acompanhados dos respectivos erros.
    """

    if not isinstance(dados, list):
        raise TypeError("Os dados devem ser uma lista de registros.")

    if not dados:
        raise ValueError("A lista de dados está vazia.")

    # Identificar todos os indicadores esperados:

    campos_kpi = set()

    for registro in dados:
        if isinstance(registro, dict):
            campos_kpi.update(identificar_campos_kpi(registro))

    if not campos_kpi:
        raise ValueError(
            "Nenhum indicador do CAGED foi encontrado. "
            "Esperados campos como admissoes_202601 e saldo_202601."
        )

    # Verificar se cada mês possui os dois indicadores:

    meses = {
        campo.split("_", 1)[1]
        for campo in campos_kpi
    }

    for mes in meses:
        if not mes.isdigit() or len(mes) != 6:
            raise ValueError(
                f"Período mensal inválido nos indicadores: {mes}."
            )

        if f"admissoes_{mes}" not in campos_kpi:
            raise ValueError(
                f"Indicador de admissões ausente para o período {mes}."
            )

        if f"saldo_{mes}" not in campos_kpi:
            raise ValueError(
                f"Indicador de saldo ausente para o período {mes}."
            )

    # Contar os IDs para identificar municípios duplicados:

    ids = [
        registro.get("id_municipio")
        for registro in dados
        if isinstance(registro, dict)
    ]

    contagem_ids = Counter(ids)

    dados_validos = []
    dados_invalidos = []

    # Validar cada registro:

    for registro in dados:

        erros = []

        if not isinstance(registro, dict):
            dados_invalidos.append({
                "registro": registro,
                "erros": ["O registro não é um dicionário."],
            })
            continue

        # Verificar os campos obrigatórios:

        for campo in CAMPOS_OBRIGATORIOS:

            if campo not in registro:
                erros.append(f"Campo obrigatório ausente: {campo}.")

            elif registro[campo] is None:
                erros.append(f"O campo {campo} está vazio.")

            elif (
                isinstance(registro[campo], str)
                and not registro[campo].strip()
            ):
                erros.append(f"O campo {campo} está vazio.")

        # Validar o código IBGE do município:

        id_municipio = registro.get("id_municipio")

        if not isinstance(id_municipio, str):
            erros.append("O ID do município deve ser str.")

        else:
            if id_municipio != id_municipio.strip():
                erros.append("O ID possui espaços extras.")

            if not id_municipio.isdigit() or len(id_municipio) != 7:
                erros.append(
                    "O ID deve ser um código IBGE de 7 dígitos."
                )

            if contagem_ids[id_municipio] > 1:
                erros.append(
                    f"ID de município duplicado: {id_municipio}."
                )

        # Validar o nome do município:

        municipio = registro.get("municipio")

        if isinstance(municipio, str):
            if municipio != municipio.strip():
                erros.append(
                    "O nome do município possui espaços extras."
                )

            if municipio.endswith("- SC"):
                erros.append(
                    "O nome ainda contém o sufixo '- SC'."
                )

        elif municipio is not None:
            erros.append("O nome do município deve ser str.")

        # Verificar indicadores ausentes ou inesperados:

        campos_presentes = identificar_campos_kpi(registro)

        campos_ausentes = campos_kpi - campos_presentes
        campos_extras = campos_presentes - campos_kpi

        if campos_ausentes:
            erros.append(
                f"Indicadores mensais ausentes: {sorted(campos_ausentes)}."
            )

        if campos_extras:
            erros.append(
                f"Indicadores mensais inesperados: {sorted(campos_extras)}."
            )

        # Validar os valores dos indicadores:

        for campo in campos_presentes:

            valor = registro[campo]

            if type(valor) is not int:
                erros.append(
                    f"{campo} deve ser int; "
                    f"recebido: {type(valor).__name__}."
                )
                continue

            # Admissões não podem ser negativas.
            if campo.startswith("admissoes_") and valor < 0:
                erros.append(
                    f"{campo} não pode ter valor negativo."
                )

            # Saldos podem ser negativos no Novo CAGED.

        # Separar registros válidos e inválidos:

        if erros:
            dados_invalidos.append({
                "registro": registro,
                "erros": erros,
            })
        else:
            dados_validos.append(registro)

    return dados_validos, dados_invalidos


# Testando a validação:

if __name__ == "__main__":

    dados_teste = [
        {
            "id_municipio": "4200051",
            "municipio": "Abdon Batista",
            "admissoes_202601": 10,
            "saldo_202601": -2,
            "admissoes_202602": 8,
            "saldo_202602": 1,
        },
        {
            "id_municipio": "4200101",
            "municipio": "Abelardo Luz",
            "admissoes_202601": 7,
            "saldo_202601": 2,
            "admissoes_202602": 4,
            "saldo_202602": -1,
        },
    ]

    validos, invalidos = validar_dados(dados_teste)

    print(f"Registros recebidos: {len(dados_teste)}")
    print(f"Registros válidos: {len(validos)}")
    print(f"Registros inválidos: {len(invalidos)}")

    if invalidos:
        print("\nPrimeiros registros inválidos:")

        for item in invalidos[:5]:
            print(item)
