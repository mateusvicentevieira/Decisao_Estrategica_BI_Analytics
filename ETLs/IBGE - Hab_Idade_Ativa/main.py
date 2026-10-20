# Bibliotecas e importações:

from extract import extrair_dados
from transform import transformar_dados
from validate import validar_dados
from aggregate import agregar_dados
from load import carregar_dados


# Executando o ETL completo:

def executar_etl():

    print("\nIniciando o ETL de população por faixa etária...\n")

    # 1. Extração:

    print("Etapa 1/5: Extraindo dados da API do IBGE...")

    dados_extraidos = extrair_dados()

    print(f"Registros extraídos: {len(dados_extraidos)}")

    # 2. Transformação:

    print("\nEtapa 2/5: Transformando os dados...")

    dados_transformados = transformar_dados(
        dados_extraidos
    )

    print(f"Registros transformados: {len(dados_transformados)}")

    # 3. Validação:

    print("\nEtapa 3/5: Validando os dados...")

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

    # 4. Agregação:

    print("\nEtapa 4/5: Agregando as faixas etárias...")

    dados_agregados = agregar_dados(
        dados_validos
    )

    print(f"Registros agregados: {len(dados_agregados)}")

    # 5. Carga:

    print("\nEtapa 5/5: Carregando dados no PostgreSQL...")

    total_carregado = carregar_dados(
        dados_agregados
    )

    # Relatório final:

    print("\nETL finalizado!")

    print(f"Total extraído: {len(dados_extraidos)}")
    print(f"Total válido: {len(dados_validos)}")
    print(f"Total inválido: {len(dados_invalidos)}")
    print(f"Total agregado: {len(dados_agregados)}")
    print(f"Total carregado ou atualizado: {total_carregado}")


# Executando somente quando o arquivo for iniciado diretamente:

if __name__ == "__main__":

    executar_etl()
