# Bibliotecas e importações:

from extract import extrair_dados
from aggregate import agregar_dados
from transform import transformar_dados
from validate import validar_dados
from load import carregar_dados


# Executando o ETL completo:

def executar_etl():

    print("\nIniciando o ETL de crescimento de domicílios por município...\n")

    # 1. Extração:

    print("Etapa 1/5: Extraindo dados das APIs do IBGE (2022, 2010, 2000, 1991, 1980)...")

    (
        dados_extraidos_2022,
        dados_extraidos_2010,
        dados_extraidos_2000,
        dados_extraidos_1991,
        dados_extraidos_1980
    ) = extrair_dados()

    print(f"2022 - Registros extraídos: {len(dados_extraidos_2022)}")
    print(f"2010 - Registros extraídos: {len(dados_extraidos_2010)}")
    print(f"2000 - Registros extraídos: {len(dados_extraidos_2000)}")
    print(f"1991 - Registros extraídos: {len(dados_extraidos_1991)}")
    print(f"1980 - Registros extraídos: {len(dados_extraidos_1980)}")

    # 2. Agregação:

    print("\nEtapa 2/5: Agregando dados das APIs por município em linha única...")

    dados_agregados = agregar_dados(
        dados_extraidos_2022,
        dados_extraidos_2010,
        dados_extraidos_2000,
        dados_extraidos_1991,
        dados_extraidos_1980
    )

    print(f"Registros agregados: {len(dados_agregados)}")

    # 3. Transformação:

    print("\nEtapa 3/5: Transformando os dados...")

    dados_transformados = transformar_dados(
        dados_agregados
    )

    print(f"Registros transformados: {len(dados_transformados)}")

    # 4. Validação:

    print("\nEtapa 4/5: Validando os dados...")

    dados_validos, dados_invalidos = validar_dados(
        dados_transformados
    )

    print(f"Registros válidos: {len(dados_validos)}")
    print(f"Registros inválidos: {len(dados_invalidos)}")

    # Exibindo os erros encontrados:

    if dados_invalidos:

        print("\nExemplos de registros inválidos:")

        for item in dados_invalidos[:5]:
            print(item)

        if not dados_validos:
            raise ValueError(
                "A etapa de validação falhou: nenhum registro válido para prosseguir."
            )

    # 5. Carga:

    print("\nEtapa 5/5: Carregando dados no PostgreSQL...")

    total_carregado = carregar_dados(
        dados_validos
    )

    # Relatório final:

    print("\nETL finalizado com sucesso!")

    print(f"Total agregado: {len(dados_agregados)}")
    print(f"Total válido: {len(dados_validos)}")
    print(f"Total inválido: {len(dados_invalidos)}")
    print(f"Total carregado ou atualizado: {total_carregado}")

    return total_carregado


# Executando somente quando o arquivo for iniciado diretamente:

if __name__ == "__main__":

    executar_etl()
