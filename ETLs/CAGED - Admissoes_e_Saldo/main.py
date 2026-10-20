
# Bibliotecas e importações:

from time import perf_counter

from extract import extrair_dados
from transform import transformar_dados
from aggregate import agregar_dados
from validate import validar_dados
from load import carregar_dados


# Executando a pipeline ETL:

def executar_etl():
    """Executa a pipeline ETL do Novo CAGED."""

    inicio_total = perf_counter()

    print("Iniciando ETL do Novo CAGED...\n")

    # Extração:

    inicio = perf_counter()

    dados_extraidos = list(extrair_dados())

    print(
        f"Extração concluída: {len(dados_extraidos):,} "
        f"registros municipais-mês em "
        f"{perf_counter() - inicio:.2f} segundos."
    )

    # Transformação:

    inicio = perf_counter()

    dados_transformados = list(
        transformar_dados(dados_extraidos)
    )

    print(
        f"Transformação concluída: "
        f"{len(dados_transformados):,} registros em "
        f"{perf_counter() - inicio:.2f} segundos."
    )

    del dados_extraidos

    # Agregação:

    inicio = perf_counter()

    dados_agregados = agregar_dados(dados_transformados)

    print(
        f"Agregação concluída: {len(dados_agregados):,} "
        f"municípios em {perf_counter() - inicio:.2f} segundos."
    )

    del dados_transformados

    # Validação:

    inicio = perf_counter()

    dados_validos, dados_invalidos = validar_dados(
        dados_agregados
    )

    print(
        f"Validação concluída em "
        f"{perf_counter() - inicio:.2f} segundos."
    )

    print(f"Registros válidos: {len(dados_validos):,}")
    print(f"Registros inválidos: {len(dados_invalidos):,}")

    del dados_agregados

    # Exibir alguns erros encontrados:

    if dados_invalidos:
        print("\nExemplos de registros inválidos:")

        for item in dados_invalidos[:5]:
            print(item)

    # Interromper a carga se não houver registros válidos:

    if not dados_validos:
        raise ValueError(
            "Nenhum registro válido foi encontrado. "
            "A carga no PostgreSQL foi cancelada."
        )

    # Carga:

    inicio = perf_counter()

    total_carregado = carregar_dados(dados_validos)

    print(
        f"Carga concluída: {total_carregado:,} registros "
        f"em {perf_counter() - inicio:.2f} segundos."
    )

    # Relatório final:

    print(
        f"\nETL finalizado em "
        f"{perf_counter() - inicio_total:.2f} segundos."
    )


if __name__ == "__main__":
    executar_etl()
