
# Bibliotecas e importações:

from typing import Any, Dict, Iterable, List


# Agregando os dados por município:

def agregar_dados(
    dados_validos: Iterable[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """Consolida os indicadores mensais em um registro por município."""

    dados_agregados: Dict[str, Dict[str, Any]] = {}

    for registro in dados_validos:

        # Verificar a estrutura do registro:

        if not isinstance(registro, dict):
            raise TypeError(
                f"O registro deve ser um dicionário: {registro}"
            )

        if "id_municipio" not in registro or "municipio" not in registro:
            raise ValueError(
                f"Registro sem identificação do município: {registro}"
            )

        id_municipio = registro["id_municipio"]
        municipio = registro["municipio"]

        # Criar o registro do município, caso ainda não exista:

        if id_municipio not in dados_agregados:
            dados_agregados[id_municipio] = {
                "id_municipio": id_municipio,
                "municipio": municipio,
            }

        registro_agregado = dados_agregados[id_municipio]

        # Consolidar os indicadores mensais:

        for campo, valor in registro.items():

            if campo.startswith("admissoes_") or campo.startswith("saldo_"):

                # Evitar sobrescrever silenciosamente um indicador repetido:

                if campo in registro_agregado:
                    raise ValueError(
                        f"Indicador duplicado para o município "
                        f"{id_municipio}: {campo}"
                    )

                registro_agregado[campo] = valor

    return list(dados_agregados.values())


# Testando a agregação:

if __name__ == "__main__":

    dados_teste = [
        {
            "id_municipio": "4200051",
            "municipio": "Abdon Batista",
            "admissoes_202601": 10,
            "saldo_202601": 2,
        },
        {
            "id_municipio": "4200051",
            "municipio": "Abdon Batista",
            "admissoes_202602": 5,
            "saldo_202602": -1,
        },
        {
            "id_municipio": "4200101",
            "municipio": "Abelardo Luz",
            "admissoes_202601": 7,
            "saldo_202601": 0,
        },
    ]

    dados_agregados = agregar_dados(dados_teste)

    print(f"Municípios agregados: {len(dados_agregados)}")
    print("\nPrimeiros registros:")

    for registro in dados_agregados[:5]:
        print(registro)
