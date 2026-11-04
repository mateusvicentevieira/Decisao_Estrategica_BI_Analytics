"""Valida a identidade municipal antes da carga."""

def validar_registros(dados):
    vistos = set()
    for linha in dados:
        codigo = linha["id_municipio"]
        if not codigo or not linha["municipio"] or codigo in vistos:
            raise ValueError("Município sem identificação ou duplicado.")
        vistos.add(codigo)
    return dados, [], []

def exibir_relatorio(dados, validos, invalidos, duplicados):
    print(f"Municípios válidos: {len(validos)}")
