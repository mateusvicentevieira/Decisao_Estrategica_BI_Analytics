
# Bibliotecas e importações:

from extract import extrair_dados
from validate import validar_registros, exibir_relatorio
from transform import transformar_dados
from load import carregar_dados


# Executando o pipeline ETL:

def executar_pipeline():

    # Etapa 1: Extraindo os dados:

    print("\nIniciando a extração dos dados...")

    dados_extraidos = extrair_dados()

    print(f"Registros extraídos: {len(dados_extraidos)}")

    # Etapa 2: Validando os dados:

    print("\nIniciando a validação dos dados...")

    dados_validos, dados_invalidos, duplicados = validar_registros(
        dados_extraidos
    )

    exibir_relatorio(
        dados_extraidos,
        dados_validos,
        dados_invalidos,
        duplicados
    )

    # Etapa 3: Transformando os dados:

    print("\nIniciando a transformação dos dados...")

    dados_transformados = transformar_dados(dados_validos)

    print(f"Registros transformados: {len(dados_transformados)}")

    # Etapa 4: Carregando os dados:

    print("\nIniciando a carga no PostgreSQL...")

    total_carregado = carregar_dados(dados_transformados)

    # Etapa 5: Exibindo o relatório final:

    print("\nProcesso ETL finalizado.")

    print(f"Registros extraídos: {len(dados_extraidos)}")
    print(f"Registros inválidos: {len(dados_invalidos)}")
    print(f"Registros duplicados identificados: {len(duplicados)}")
    print(f"Registros transformados: {len(dados_transformados)}")
    print(f"Registros carregados: {total_carregado}")


# Executando o pipeline apenas quando este arquivo for executado diretamente:

if __name__ == "__main__":

    executar_pipeline()
