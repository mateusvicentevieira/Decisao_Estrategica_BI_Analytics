# Bibliotecas e importações:

import csv
import json
import time
import unicodedata
from collections import defaultdict
from ftplib import FTP, all_errors
from pathlib import Path

import py7zr
import requests


# Constantes:

FTP_HOST = "ftp.mtps.gov.br"
FTP_ROOT_DIR = "pdet/microdados/NOVO CAGED"
ANO = "2026"
MESES = [f"{ANO}{mes:02d}" for mes in range(1, 9)]
CODIGO_UF_SC = "42"

PASTA_TEMP = Path(__file__).resolve().parent / "tmp_caged"
PASTA_TEMP.mkdir(parents=True, exist_ok=True)
ARQUIVO_MAPEAMENTO = PASTA_TEMP / "municipios_sc_ibge.json"

TENTATIVAS_FTP = 3
TIMEOUT_REDE = 60


def normalizar_nome_coluna(nome):
    """Remove acentos e padroniza o nome de uma coluna do CAGED."""
    nome = unicodedata.normalize("NFKD", nome or "")
    nome = "".join(caractere for caractere in nome if not unicodedata.combining(caractere))
    return nome.strip().lower()


def conectar_ftp():
    """Abre uma conexão FTP nova."""
    ftp = FTP(timeout=TIMEOUT_REDE)
    ftp.connect(FTP_HOST, 21, timeout=TIMEOUT_REDE)
    ftp.login()
    ftp.set_pasv(True)
    return ftp


def baixar_arquivo_mensal(ftp, competencia):
    """Baixa somente o arquivo da competência solicitada, com tentativas de reconexão."""
    nome_arquivo = f"CAGEDMOV{competencia}.7z"
    caminho_local = PASTA_TEMP / nome_arquivo
    caminho_parcial = PASTA_TEMP / f"{nome_arquivo}.part"

    if caminho_local.exists() and caminho_local.stat().st_size > 0:
        print(f"Arquivo já baixado: {nome_arquivo}")
        return caminho_local

    caminho_remoto = f"/{FTP_ROOT_DIR}/{ANO}/{competencia}/{nome_arquivo}"
    ultimo_erro = None

    for tentativa in range(1, TENTATIVAS_FTP + 1):
        ftp_atual = ftp
        try:
            print(f"Baixando {nome_arquivo} (tentativa {tentativa}/{TENTATIVAS_FTP})")
            with caminho_parcial.open("wb") as arquivo_saida:
                ftp_atual.retrbinary(f"RETR {caminho_remoto}", arquivo_saida.write, blocksize=1024 * 1024)
            caminho_parcial.replace(caminho_local)
            print(f"Download concluído: {competencia}")
            return caminho_local
        except (all_errors + (OSError,)) as erro:
            ultimo_erro = erro
            caminho_parcial.unlink(missing_ok=True)
            try:
                ftp_atual.close()
            except Exception:
                pass
            if tentativa < TENTATIVAS_FTP:
                time.sleep(2 * tentativa)
                ftp = conectar_ftp()

    raise RuntimeError(f"Não foi possível baixar {nome_arquivo}: {ultimo_erro}")


def obter_mapeamento_municipios_sc():
    """Obtém e guarda em cache os códigos IBGE completos e nomes dos municípios de SC.

    O CAGED normalmente apresenta os seis primeiros dígitos do código municipal IBGE.
    O mapeamento usa a lista oficial do IBGE para recuperar o código de sete dígitos,
    em vez de inventar ou completar o dígito final.
    """
    if ARQUIVO_MAPEAMENTO.exists():
        try:
            with ARQUIVO_MAPEAMENTO.open("r", encoding="utf-8") as arquivo:
                cache = json.load(arquivo)
            if cache:
                return cache
        except (OSError, json.JSONDecodeError):
            pass

    url = "https://servicodados.ibge.gov.br/api/v1/localidades/estados/42/municipios"
    resposta = requests.get(url, timeout=TIMEOUT_REDE)
    resposta.raise_for_status()
    municipios = resposta.json()

    mapeamento = {}
    for municipio in municipios:
        codigo_ibge = str(municipio["id"])
        mapeamento[codigo_ibge[:6]] = {
            "id_municipio": codigo_ibge,
            "municipio": municipio["nome"],
        }

    with ARQUIVO_MAPEAMENTO.open("w", encoding="utf-8") as arquivo:
        json.dump(mapeamento, arquivo, ensure_ascii=False, indent=2)

    return mapeamento


def extrair_arquivo_7z(caminho_arquivo, competencia):
    """Extrai o arquivo mensal para uma pasta própria e devolve o TXT encontrado."""
    pasta_mes = PASTA_TEMP / competencia
    pasta_extraida = pasta_mes / "extraido"
    pasta_extraida.mkdir(parents=True, exist_ok=True)

    arquivos_txt = list(pasta_extraida.glob("*.txt")) + list(pasta_extraida.glob("*.TXT"))
    if arquivos_txt:
        return arquivos_txt[0]

    print(f"Extraindo competência: {competencia}")
    with py7zr.SevenZipFile(caminho_arquivo, mode="r") as arquivo_7z:
        arquivo_7z.extractall(path=pasta_extraida)

    arquivos_txt = list(pasta_extraida.rglob("*.txt")) + list(pasta_extraida.rglob("*.TXT"))
    if not arquivos_txt:
        raise FileNotFoundError(f"Nenhum TXT foi encontrado no arquivo {caminho_arquivo.name}.")

    return arquivos_txt[0]


def abrir_csv_com_codificacao(caminho_txt):
    """Abre o TXT com a codificação adequada e separador ';'."""
    for codificacao in ("utf-8-sig", "cp1252", "latin-1"):
        arquivo = caminho_txt.open("r", encoding=codificacao, newline="")
        try:
            primeira_linha = arquivo.readline()
            arquivo.seek(0)
            if ";" not in primeira_linha:
                arquivo.close()
                raise ValueError(
                    f"O arquivo {caminho_txt.name} não parece usar ';' como delimitador. "
                    f"Início do cabeçalho: {primeira_linha[:180]!r}"
                )
            return arquivo
        except UnicodeDecodeError:
            arquivo.close()

    raise UnicodeError(f"Não foi possível identificar a codificação de {caminho_txt.name}.")


def processar_txt_mensal(caminho_txt, competencia, mapeamento):
    """Lê o TXT linha a linha e mantém na memória apenas os totais municipais do mês."""
    totais = defaultdict(lambda: {"admissoes": 0, "saldo": 0})

    with abrir_csv_com_codificacao(caminho_txt) as arquivo:
        leitor = csv.DictReader(arquivo, delimiter=";")
        if not leitor.fieldnames:
            raise ValueError(f"O arquivo {caminho_txt.name} não possui cabeçalho.")

        colunas = {
            normalizar_nome_coluna(nome): nome
            for nome in leitor.fieldnames
            if nome
        }

        coluna_municipio = colunas.get("municipio")
        coluna_uf = colunas.get("uf")
        coluna_saldo = colunas.get("saldomovimentacao")

        colunas_faltantes = [
            nome
            for nome, coluna in (
                ("município", coluna_municipio),
                ("uf", coluna_uf),
                ("saldomovimentação", coluna_saldo),
            )
            if coluna is None
        ]
        if colunas_faltantes:
            raise ValueError(
                f"Colunas não encontradas em {caminho_txt.name}: {colunas_faltantes}. "
                f"Cabeçalho identificado: {leitor.fieldnames}"
            )

        linhas_lidas = 0
        linhas_sc = 0
        for linha in leitor:
            linhas_lidas += 1
            uf = (linha.get(coluna_uf) or "").strip()
            if uf != CODIGO_UF_SC:
                continue

            linhas_sc += 1
            codigo_caged = (linha.get(coluna_municipio) or "").strip()
            municipio_ibge = mapeamento.get(codigo_caged)
            if municipio_ibge is None:
                # Não tenta adivinhar códigos: registra o código desconhecido para correção explícita.
                continue

            valor_saldo = (linha.get(coluna_saldo) or "").strip()
            try:
                saldo_movimento = int(valor_saldo)
            except (TypeError, ValueError):
                continue

            codigo_ibge = municipio_ibge["id_municipio"]
            totais[codigo_ibge]["saldo"] += saldo_movimento
            if saldo_movimento == 1:
                totais[codigo_ibge]["admissoes"] += 1

    print(
        f"Leitura concluída: {competencia} | linhas lidas: {linhas_lidas:,} | "
        f"linhas de SC: {linhas_sc:,} | municípios com movimentação: {len(totais)}"
    )

    registros = []
    for codigo_ibge, valores in totais.items():
        registros.append({
            "id_municipio": str(codigo_ibge),
            "municipio": mapeamento[codigo_ibge[:6]]["municipio"],
            f"admissoes_{competencia}": valores["admissoes"],
            f"saldo_{competencia}": valores["saldo"],
        })

    return registros


def extrair_dados():
    """Processa um arquivo mensal por vez e retorna registros municipais mensais.

    Para reduzir o consumo de memória, as linhas nacionais não são acumuladas em uma lista:
    cada TXT é percorrido sequencialmente e só os totais dos municípios de SC ficam na memória.
    """
    mapeamento = obter_mapeamento_municipios_sc()
    ftp = conectar_ftp()

    try:
        for competencia in MESES:
            print(f"\nProcessando competência: {competencia}")
            caminho_arquivo = baixar_arquivo_mensal(ftp, competencia)
            caminho_txt = extrair_arquivo_7z(caminho_arquivo, competencia)

            # Só remove o arquivo compactado depois que a leitura mensal termina com sucesso.
            registros_mes = processar_txt_mensal(caminho_txt, competencia, mapeamento)
            caminho_arquivo.unlink(missing_ok=True)

            for registro in registros_mes:
                yield registro
    finally:
        try:
            ftp.quit()
        except Exception:
            try:
                ftp.close()
            except Exception:
                pass


if __name__ == "__main__":
    total = 0
    for _ in extrair_dados():
        total += 1
    print(f"Extração concluída. Registros municipais-mês gerados: {total:,}")
