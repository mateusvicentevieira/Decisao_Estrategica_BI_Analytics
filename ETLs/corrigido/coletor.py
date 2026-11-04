"""Coleta oficial auditável; --carregar cria novas tabelas e preserva public."""
from pathlib import Path
from decimal import Decimal, InvalidOperation
from datetime import datetime, timezone
import argparse
import hashlib
import json
import re
import requests

HERE = Path(__file__).resolve().parent
BASE = 'https://servicodados.ibge.gov.br/api/v3/agregados/'


def numero(valor):
    if valor is None or str(valor).strip() in ('', '...', '..', 'X'):
        return None
    if str(valor).strip() == '-':
        return Decimal(0)  # Convenção IBGE/SIDRA: zero absoluto publicado.
    try:
        n = Decimal(str(valor).strip().replace(',', '.'))
        return n if n.is_finite() else None
    except InvalidOperation:
        return None


def validar_categorias(categorias):
    codigos = [re.sub(r'[^0-9]', '', x) for x in categorias]
    if len(set(codigos)) != len(codigos):
        raise ValueError('Categoria duplicada')
    if any(a != b and b.startswith(a) for a in codigos for b in codigos):
        raise ValueError('Categorias CNAE sobrepostas')


def agregar_exclusivas(valores):
    validar_categorias([x[0] for x in valores])
    return None if any(x[1] is None for x in valores) else sum(x[1] for x in valores)


def alinhar_periodos(periodos):
    if len(set(periodos)) != 1:
        raise ValueError('Componentes de períodos diferentes')
    return periodos[0]


def validar_cobertura(ids, esperados):
    if len(ids) != len(set(ids)) or set(ids) != set(esperados):
        raise ValueError('Cobertura ou chave municipal inválida')


def movimento_construcao(linha):
    """Filtro aplicável ao microdado CAGED antes de qualquer agregação."""
    if linha.get('secao'):
        return str(linha['secao']).strip().upper() == 'F'
    if linha.get('subclasse'):
        return str(linha['subclasse']).strip().zfill(7)[:2] in ('41', '42', '43')
    raise ValueError('Microdado sem seção ou subclasse CNAE')


def obter(url):
    r = requests.get(url, timeout=90)
    r.raise_for_status()
    return r.json()


# A categoria 47.4 é usada uma única vez, sem somar suas classes filhas.
# Não é necessário somar classes suprimidas para obter o agregado publicado.
FONTES = [
    ('populacao', '4709', '93', '2022', '', 'Pessoas', 'População residente total'),
    ('domicilios', '4712', '381', '2022', '', 'Domicílios', 'Domicílios particulares permanentes ocupados'),
    ('renda', '10289', '13537', '2022', '2[6794]|86[95251]', 'Reais', 'Rendimento nominal mediano mensal de todos os trabalhos; ocupados de 14 anos ou mais com rendimento de trabalho'),
    ('ocupados', '10268', '696', '2022', '2[6794]|86[95251]|58[82072]', 'Pessoas', 'Pessoas de 14 anos ou mais ocupadas na semana de referência'),
    ('populacao_14mais', '10268', '140', '2022', '2[6794]|86[95251]|58[82072]', 'Pessoas', 'Pessoas de 14 anos ou mais; mesmo universo de ocupados'),
    *[('concorrentes', '9528', '706', ano, '12762[117452]', 'Unidades', 'Unidades locais; CNAE grupo 47.4 comércio varejista de material de construção; agregado exclusivo') for ano in ('2022','2023','2024')],
]


def coletar():
    run = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
    pasta = HERE / 'dados' / run
    pasta.mkdir(parents=True, exist_ok=False)
    municipios = obter('https://servicodados.ibge.gov.br/api/v1/localidades/estados/42/municipios')
    municipios = {str(x['id']): x['nome'] for x in municipios}
    if len(municipios) != 295:
        raise ValueError('Cadastro SC não contém 295 municípios')
    manifest = {'versao': run, 'coletado_em': datetime.now(timezone.utc).isoformat(), 'municipios':295,
                'fontes':[], 'limitacoes':[
                    'Concorrência é proxy de unidades locais do grupo CNAE 47.4; não identifica redes nem capacidades comerciais.',
                    'CEMPRE 2022 inicia nova série; não comparar diretamente com série encerrada em 2021.',
                    'Renda nominal de 2022 não equivale a renda domiciliar per capita nem renda atual.',
                    'CAGED public contém todos setores; não foi incluído nem recolhido por demandar grandes microdados.',
                    'Histórico antigo de domicílios em public não é utilizado por incompatibilidade de universo.',
                    'Símbolos de ausência ou supressão X/../... são NULL; hífen representa zero absoluto publicado conforme convenção IBGE/SIDRA. Valor bruto preservado.',
                    'Legenda oficial: https://www.ibge.gov.br/explica/producao-agropecuaria/pa (sinais convencionais IBGE).'
                ]}
    linhas = []
    metas = {}
    for kpi, agregado, variavel, periodo, classificacao, unidade, universo in FONTES:
        url = f'{BASE}{agregado}/periodos/{periodo}/variaveis/{variavel}?localidades=N6[N3[42]]'
        if classificacao:
            url += '&classificacao=' + classificacao
        if agregado not in metas:
            metas[agregado] = obter(BASE + agregado + '/metadados')
            (pasta / f'metadados_{agregado}.json').write_text(json.dumps(metas[agregado],ensure_ascii=False,indent=2),encoding='utf-8')
        meta = metas[agregado]
        vm = next(x for x in meta['variaveis'] if str(x['id']) == variavel)
        if vm['unidade'] != unidade:
            raise ValueError('Unidade não corresponde ao contrato')
        dados = obter(url)
        texto = json.dumps(dados, ensure_ascii=False, indent=2)
        (pasta / f'{kpi}_{periodo}.json').write_text(texto,encoding='utf-8')
        series = [s for item in dados for resultado in item['resultados'] for s in resultado['series']]
        validar_cobertura([s['localidade']['id'] for s in series], municipios)
        validos = 0
        for s in series:
            mid = s['localidade']['id']
            bruto = s['serie'].get(periodo)
            valor = numero(bruto)
            if valor is not None and valor < 0:
                raise ValueError('Fonte de contagem/renda negativa')
            validos += valor is not None
            linhas.append({'id_municipio':mid,'municipio':municipios[mid],'kpi':kpi,'periodo':int(periodo),
                           'valor':str(valor) if valor is not None else None,'valor_bruto':bruto,'unidade':unidade,
                           'universo':universo,'fonte':url,'agregado':agregado,'variavel':variavel,
                           'classificacao':classificacao,'coletado_em':manifest['coletado_em']})
        manifest['fontes'].append({'kpi':kpi,'periodo':periodo,'fonte':url,'universo':universo,
            'unidade':unidade,'variavel_nome':vm['nome'],'cobertura':len(series),'valores_validos':validos,
            'sha256':hashlib.sha256(texto.encode()).hexdigest()})
        print(kpi, periodo, len(series), 'válidos',validos,flush=True)
    # Integridade das duas variáveis que formam a taxa contemporânea.
    pivot = {(r['id_municipio'],r['kpi'],r['periodo']):numero(r['valor']) for r in linhas}
    for mid in municipios:
        a=pivot[mid,'ocupados',2022]; b=pivot[mid,'populacao_14mais',2022]
        alinhar_periodos([2022,2022])
        if a is not None and b is not None and (b <= 0 or a > b):
            raise ValueError('Ocupados incompatíveis com denominador 14+')
    (pasta/'fontes.json').write_text(json.dumps(linhas,ensure_ascii=False,indent=2),encoding='utf-8')
    (pasta/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    return run, pasta, linhas, manifest


def carregar(run, linhas, manifest):
    import psycopg
    from psycopg import sql
    from dotenv import dotenv_values
    raiz = HERE.parents[2]
    env = raiz / 'ETLs/IBGE - Rendimento_Mediano/.env'
    if not env.exists():
        env = raiz.parent / 'ETLs/IBGE - Rendimento_Mediano/.env'
    c=dotenv_values(env)
    params={k:c.get('DB_'+v) for k,v in [('host','HOST'),('port','PORT'),('dbname','NAME'),('user','USER'),('password','PASSWORD')]}
    nome='fontes_'+run
    with psycopg.connect(**params, connect_timeout=10) as db:
        db.execute('CREATE SCHEMA IF NOT EXISTS bi_validado')
        db.execute(sql.SQL('CREATE TABLE bi_validado.{} (id_municipio text NOT NULL, municipio text NOT NULL, kpi text NOT NULL, periodo integer NOT NULL, valor numeric, valor_bruto text, unidade text NOT NULL, universo text NOT NULL, fonte text NOT NULL, agregado text NOT NULL, variavel text NOT NULL, classificacao text NOT NULL, coletado_em timestamptz NOT NULL, PRIMARY KEY(id_municipio,kpi,periodo))').format(sql.Identifier(nome)))
        campos=list(linhas[0])
        query=sql.SQL('INSERT INTO bi_validado.{} ({}) VALUES ({})').format(sql.Identifier(nome),sql.SQL(',').join(map(sql.Identifier,campos)),sql.SQL(',').join(sql.Placeholder() for _ in campos))
        with db.cursor() as cur:
            cur.executemany(query,[[r[x] for x in campos] for r in linhas])
        total=db.execute(sql.SQL('SELECT count(*) FROM bi_validado.{}').format(sql.Identifier(nome))).fetchone()[0]
        if total != len(linhas):raise ValueError('Contagem da carga divergiu')
        db.execute(sql.SQL('COMMENT ON TABLE bi_validado.{} IS {}').format(sql.Identifier(nome),sql.Literal(json.dumps(manifest,ensure_ascii=False))))
    print('CARGA CONFIRMADA', 'bi_validado.'+nome,len(linhas),flush=True)
    return 'bi_validado.'+nome


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--carregar',action='store_true');args=p.parse_args()
    run,pasta,linhas,manifest=coletar()
    if args.carregar:
        manifest['tabela']=carregar(run,linhas,manifest)
        (pasta/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    print('MANIFEST',pasta/'manifest.json',flush=True)
