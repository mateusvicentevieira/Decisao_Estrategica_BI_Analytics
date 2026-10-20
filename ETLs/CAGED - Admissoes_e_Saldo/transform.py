
# Bibliotecas e importações:

from typing import Dict, Generator, Iterable, Any


# Funções auxiliares:

def padronizar_municipio(municipio: str) -> str:
    """Remove o sufixo '- SC' e espaços extras do nome do município."""

    municipio = municipio.strip()

    if municipio.endswith("- SC"):
        municipio = municipio[:-5]

    return municipio.strip()


def tratar_admissoes(valor: Any) -> int:
    """Converte admissões para inteiro não negativo."""

    if valor is None:
        return 0

    if isinstance(valor, bool):
        return 0

    if isinstance(valor, int):
        return valor if valor >= 0 else 0

    if not isinstance(valor, str):
        return 0

    valor = valor.strip()

    if valor in ("", "-"):
        return 0

    try:
        valor_convertido = int(valor)
    except (ValueError, TypeError):
        return 0

    return valor_convertido if valor_convertido >= 0 else 0


def tratar_saldo(valor: Any) -> int:
    """Converte o saldo para inteiro, preservando valores negativos."""

    if valor is None:
        return 0

    if isinstance(valor, bool):
        return 0

    if isinstance(valor, int):
        return valor

    if not isinstance(valor, str):
        return 0

    valor = valor.strip()

    if valor in ("", "-"):
        return 0

    try:
        return int(valor)
    except (ValueError, TypeError):
        return 0


# Transformando e padronizando os dados:

def transformar_dados(
    dados: Iterable[Dict[str, Any]]
) -> Generator[Dict[str, Any], None, None]:
    """Transforma os registros extraídos do Novo CAGED."""

    for registro in dados:

        # Verificar a estrutura do registro:

        if not isinstance(registro, dict):
            raise TypeError(
                f"O registro deve ser um dicionário: {registro}"
            )

        # Verificar os campos de identificação:

        if "id_municipio" not in registro or "municipio" not in registro:
            raise ValueError(
                f"Registro sem identificação do município: {registro}"
            )

        if registro["id_municipio"] is None:
            raise ValueError("id_municipio não pode ser None.")

        if not isinstance(registro["municipio"], str):
            raise TypeError("municipio deve ser str.")

        # Padronizar a identificação do município:

        id_municipio = str(registro["id_municipio"]).strip()
        municipio = padronizar_municipio(registro["municipio"])

        if not id_municipio or not municipio:
            raise ValueError(
                f"Identificação do município vazia: {registro}"
            )

        linha = {
            "id_municipio": id_municipio,
            "municipio": municipio,
        }

        # Tratar os indicadores mensais do Novo CAGED:

        for campo, valor in registro.items():

            if campo.startswith("admissoes_"):
                linha[campo] = tratar_admissoes(valor)

            elif campo.startswith("saldo_"):
                linha[campo] = tratar_saldo(valor)

        # Entregar um registro transformado por vez:

        yield linha


# Testando a transformação quando o arquivo é executado diretamente:

if __name__ == "__main__":

    from extract import extrair_dados

    dados_transformados = transformar_dados(extrair_dados())

    quantidade = 0

    print("Primeiros registros transformados:")

    for registro in dados_transformados:
        quantidade += 1

        if quantidade <= 5:
            print(registro)

    print(f"\nTotal de registros transformados: {quantidade}")
    