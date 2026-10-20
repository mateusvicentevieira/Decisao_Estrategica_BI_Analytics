# Bibliotecas e importações:

from extract import extrair_dados
from transform import transformar_dados
from validate import validar_dados

# Constantes:

PREFIXO_VALORES = "valor_"


# Agregando os dados por município:

def agregar_dados(dados_validos):

    dados_agregados = []

    for registro in dados_validos:

        # Somando todas as faixas etárias:

        valor_total = sum(
            valor
            for campo, valor in registro.items()
            if campo.startswith(PREFIXO_VALORES)
        )

        # Criando o registro final sem as faixas individuais:

        registro_agregado = {
            "id_municipio": registro["id_municipio"],
            "municipio": registro["municipio"],
            "valor_total": valor_total
        }

        dados_agregados.append(registro_agregado)

    return dados_agregados


# Testando a agregação:

if __name__ == "__main__":

    dados_extraidos = extrair_dados()

    dados_transformados = transformar_dados(
        dados_extraidos
    )

    dados_validos, dados_invalidos = validar_dados(
        dados_transformados
    )

    dados_agregados = agregar_dados(dados_validos)

    print(f"Registros válidos: {len(dados_validos)}")
    print(f"Registros inválidos: {len(dados_invalidos)}")
    print(f"Registros agregados: {len(dados_agregados)}")

    print("\nPrimeiros registros agregados:")

    for registro in dados_agregados[:5]:
        print(registro)
