"""Preserva os campos municipais e converte a contagem para inteiro."""

def transformar_dados(dados):
    linhas = []
    substituidos = 0
    for registro in dados:
        try:
            valor = int(registro["valor_2022"])
        except (ValueError, TypeError):
            valor = 0
            substituidos += 1
        linhas.append({**registro, "valor_2022": valor})
    print(f"Valores substituídos por zero: {substituidos}")
    return linhas
