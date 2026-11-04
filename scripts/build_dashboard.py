"""Exportação SQL somente leitura e geração reproduzível PBIP/TMDL/PBIR.

Os dados incorporados são agregados públicos exportados do banco validado.
Nenhuma conexão ou credencial é incorporada no projeto Power BI.
"""
from pathlib import Path
from decimal import Decimal
from datetime import datetime, timezone
import argparse
import json
import re
import uuid

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'dashboard'
MODEL = OUT / 'filial_construcao_sc.SemanticModel'
REPORT = OUT / 'filial_construcao_sc.Report'
SCHEMA = 'https://developer.microsoft.com/json-schemas/fabric/'
SCENARIOS = [('Referência',40,30,20,10),('Pesos iguais',25,25,25,25),('Ênfase mercado',50,25,15,10),('Menor saturação',30,25,35,10)]
COMPONENTS = [('Mercado residencial','score_domicilios','peso_mercado'),('Rendimento do trabalho','score_renda','peso_renda'),('Menor saturação','score_saturacao','peso_saturacao'),('Ocupação 14+','score_ocupacao','peso_ocupacao')]
SCORE_NAMES={'score_domicilios':'Score domicílios','score_renda':'Score renda','score_saturacao':'Score saturação','score_ocupacao':'Score ocupação'}


def normalize(values, reverse=False):
    available = [float(v) for v in values if v is not None]
    if not available or max(available) == min(available):
        return [None] * len(values)
    lo, hi = min(available), max(available)
    return [None if x is None else 100*((hi-float(x)) if reverse else (float(x)-lo))/(hi-lo) for x in values]


def weighted_index(scores, weights):
    if any(v is None for v in scores) or sum(weights) <= 0:
        return None
    return sum(v*w for v,w in zip(scores,weights))/sum(weights)


def m_value(value):
    if value is None: return 'null'
    if isinstance(value, bool): return str(value).lower()
    if isinstance(value, (float,int,Decimal)): return str(value)
    return '"'+str(value).replace('"','""').replace('\n','#(lf)').replace('\r','#(cr)')+'"'


def validate_records(records):
    seen=set()
    for r in records:
        key=(r['id_municipio'],r['kpi'],int(r['periodo']))
        if key in seen: raise ValueError('Fonte municipal duplicada')
        seen.add(key)
        if r['kpi'] != 'concorrentes' and int(r['periodo']) != 2022:
            raise ValueError('Componente fora de 2022')


def dump(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def export_sql(source):
    import psycopg
    from psycopg.rows import dict_row
    from dotenv import dotenv_values
    if not re.fullmatch(r'bi_validado\.fontes_[0-9_]+',source):
        raise ValueError('Tabela SQL deve ser snapshot versionado bi_validado.fontes_<UTC>')
    env=ROOT/'ETLs/IBGE - Rendimento_Mediano/.env'
    if not env.exists(): env=ROOT.parent/'ETLs/IBGE - Rendimento_Mediano/.env'
    c=dotenv_values(env)
    params={k:c.get('DB_'+v) for k,v in [('host','HOST'),('port','PORT'),('dbname','NAME'),('user','USER'),('password','PASSWORD')]}
    query=f'SELECT * FROM {source} ORDER BY id_municipio,kpi,periodo'
    with psycopg.connect(**params,connect_timeout=10,row_factory=dict_row) as db:
        db.execute('SET TRANSACTION READ ONLY')
        rows=db.execute(query).fetchall()
    for r in rows:
        for k,v in r.items():
            if isinstance(v,Decimal):r[k]=float(v)
            elif isinstance(v,datetime):r[k]=v.isoformat()
    validate_records(rows)
    snapshot={'fonte_sql':source,'exportado_em':datetime.now(timezone.utc).isoformat(),'linhas':rows}
    dump(OUT/'dados_snapshot.json',snapshot)
    sqlpath=ROOT/'sql/views_kpis.sql'
    sqlpath.parent.mkdir(exist_ok=True)
    sqlpath.write_text('-- Consulta somente leitura; não altera tabelas de origem.\n-- Todos os dados incorporados no PBIP são exportados desta fonte.\n'+query+';\n',encoding='utf-8')
    return snapshot


def pivot(snapshot):
    records=snapshot['linhas']; validate_records(records)
    rows={}
    for r in records:
        if r['periodo'] != 2022:continue
        mid=r['id_municipio']
        rows.setdefault(mid,{'id_municipio':mid,'municipio':r['municipio']})[r['kpi']]=r['valor']
    values=[rows[k] for k in sorted(rows)]
    if len(values)!=295:raise ValueError('Cadastro precisa conter os 295 municípios de SC')
    for r in values:
        p=r.get('populacao');d=r.get('populacao_14mais');o=r.get('ocupados');c=r.get('concorrentes')
        r['taxa_ocupacao']=100*o/d if o is not None and d is not None and d>0 else None
        r['saturacao']=10000*c/p if c is not None and p is not None and p>0 else None
        if r['taxa_ocupacao'] is not None and not 0<=r['taxa_ocupacao']<=100:raise ValueError('Taxa ocupação inválida')
    for field,score,inv in [('domicilios','score_domicilios',False),('renda','score_renda',False),('saturacao','score_saturacao',True),('taxa_ocupacao','score_ocupacao',False)]:
        for r,v in zip(values,normalize([r.get(field) for r in values],inv)):r[score]=v
    for r in values:
        r['elegivel']=int(all(r.get(c[1]) is not None for c in COMPONENTS))
    return values


def tmdl_table(name, columns, records, measures=None):
    text=f'table {name}\n\tlineageTag: {uuid.uuid5(uuid.NAMESPACE_DNS,"bi-sc."+name)}\n'
    for col,typ,fmt in columns:
        text+=f'\n\tcolumn {col}\n\t\tdataType: {typ}\n\t\tsourceColumn: {col}\n\t\tsummarizeBy: none\n'
        if fmt:text+=f'\t\tformatString: {fmt}\n'
    for m,expr,fmt in measures or []:
        text+=f"\n\tmeasure '{m}' =\n"+'\n'.join('\t\t\t'+line for line in expr.splitlines())+'\n'
        if fmt:text+=f'\t\tformatString: {fmt}\n'
    types={'string':'text','int64':'Int64.Type','double':'number','boolean':'logical'}
    mcols=', '.join(c+' = '+types[t] for c,t,_ in columns)
    mrows=',\n'.join('\t\t\t\t\t{'+', '.join(m_value(r.get(c)) for c,_,_ in columns)+'}' for r in records)
    text+=f'\n\tpartition {name} = m\n\t\tmode: import\n\t\tsource =\n\t\t\tlet\n\t\t\t\tFonte = #table(type table [{mcols}], {{\n{mrows}\n\t\t\t\t}})\n\t\t\tin\n\t\t\t\tFonte\n'
    path=MODEL/'definition/tables'/f'{name}.tmdl';path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text,encoding='utf-8')


def measures():
    result=[]
    def add(n,e,f=None):result.append((n,e,f))
    for label,field in [('Domicílios ocupados','domicilios'),('População residente','populacao'),('Rendimento mediano','renda'),('Unidades locais','concorrentes'),('Taxa de ocupação','taxa_ocupacao'),('Saturação por 10 mil','saturacao')]:
        fmt='"R$ "#,0.00' if field=='renda' else ('0.0"%"' if field=='taxa_ocupacao' else '#,0.0' if field=='saturacao' else '#,0')
        add(label,f'IF(HASONEVALUE(Municipio[id_municipio]), MAX(Fato2022[{field}]))',fmt)
    for _,score,_ in COMPONENTS:add(SCORE_NAMES[score],f'MAX(Fato2022[{score}])','0.0')
    for f,default in [('peso_mercado',40),('peso_renda',30),('peso_saturacao',20),('peso_ocupacao',10)]:add(f,f'SELECTEDVALUE(Cenario[{f}], {default})','0"%"')
    add('Cenário ativo','SELECTEDVALUE(Cenario[cenario], "Referência")')
    add('Pesos ativos','"Mercado " & FORMAT([peso_mercado],"0") & "% · Renda " & FORMAT([peso_renda],"0") & "% · Saturação " & FORMAT([peso_saturacao],"0") & "% · Ocupação " & FORMAT([peso_ocupacao],"0") & "%"')
    scoreexpr=' + '.join(f'[{SCORE_NAMES[s]}]*[{w}]' for _,s,w in COMPONENTS)
    add('Índice',f'IF(HASONEVALUE(Municipio[id_municipio]) && MAX(Fato2022[elegivel]) = 1, DIVIDE({scoreexpr}, [peso_mercado]+[peso_renda]+[peso_saturacao]+[peso_ocupacao]))','0.0')
    add('Índice municipal','IF(HASONEVALUE(Municipio[id_municipio]), [Índice])','0.0" /100"')
    add('Elegíveis','CALCULATE(COUNTROWS(Fato2022), REMOVEFILTERS(Municipio), Fato2022[elegivel]=1)','0')
    add('Cobertura','FORMAT([Elegíveis],"0") & " / 295"')
    add('Ano','2022','0')
    add('Ranking','VAR atual=[Índice]\nRETURN IF(HASONEVALUE(Municipio[id_municipio]) && NOT ISBLANK(atual), RANKX(FILTER(ALL(Municipio), CALCULATE(MAX(Fato2022[elegivel]))=1), [Índice], atual, DESC, DENSE))','0')
    add('Posição estadual','IF(HASONEVALUE(Municipio[id_municipio]), FORMAT([Ranking],"0") & " / " & FORMAT([Elegíveis],"0"), "Selecione um município")')
    add('Índice Top 10','VAR municipioSelecionado=SELECTEDVALUE(Municipio[id_municipio])\nVAR topdez=TOPN(10,FILTER(ALL(Municipio),CALCULATE(MAX(Fato2022[elegivel]))=1),[Índice],DESC,Municipio[id_municipio],ASC)\nRETURN IF(CONTAINS(topdez,Municipio[id_municipio],municipioSelecionado),[Índice])','0.0')
    add('Município líder','VAR t=TOPN(1,FILTER(ALL(Municipio),CALCULATE(MAX(Fato2022[elegivel]))=1),[Índice],DESC,Municipio[id_municipio],ASC)\nRETURN IF([Elegíveis]=0,"Sem base validada para recomendar",CONCATENATEX(t,Municipio[municipio],""))')
    add('Índice do líder','MAXX(FILTER(ALL(Municipio),CALCULATE(MAX(Fato2022[elegivel]))=1),[Índice])','0.0" /100"')
    add('Veredito','VAR nome=[Município líder]\nVAR cidade=FILTER(ALL(Municipio),Municipio[municipio]=nome)\nVAR casas=CALCULATE(MAX(Fato2022[domicilios]),cidade)\nVAR renda=CALCULATE(MAX(Fato2022[renda]),cidade)\nRETURN IF([Elegíveis]=0,"Sem base validada para recomendar",nome & " lidera o cenário " & [Cenário ativo] & " de 2022 (" & FORMAT([Índice do líder],"0.0") & "/100)." & UNICHAR(10) & FORMAT(casas,"#,0") & " domicílios ocupados e rendimento mediano do trabalho de R$ " & FORMAT(renda,"#,0") & "." & UNICHAR(10) & "Prioridade para estudo comercial; custos, logística e retorno financeiro não foram estimados.")')
    add('Resumo municipal','IF(NOT HASONEVALUE(Municipio[id_municipio]),"Selecione um município pelo nome para avaliar seus indicadores.",IF(MAX(Fato2022[elegivel])<>1,SELECTEDVALUE(Municipio[municipio]) & ": índice indisponível por ausência de concorrência publicada; ausência não é zero.",SELECTEDVALUE(Municipio[municipio]) & " · " & FORMAT([Índice],"0.0") & "/100 · " & [Cenário ativo] & UNICHAR(10) & "Ocupação 14+: " & FORMAT([Taxa de ocupação],"0.0") & "% · Saturação: " & FORMAT([Saturação],"0.0") & " unidades locais/10 mil habitantes." & UNICHAR(10) & "Compare as contribuições abaixo; a pontuação não estima retorno financeiro."))')
    add('Contribuição','IF(HASONEVALUE(Municipio[id_municipio]) && MAX(Fato2022[elegivel])=1,SWITCH(SELECTEDVALUE(Componente[componente]),'+','.join(f'"{label}",DIVIDE([{SCORE_NAMES[score]}]*[{weight}],[peso_mercado]+[peso_renda]+[peso_saturacao]+[peso_ocupacao])' for label,score,weight in COMPONENTS)+'))','0.0')
    add('Sem histórico','"Série comparável de domicílios ainda indisponível." & UNICHAR(10) & "Apenas 2022 está validado. A série anterior usa outro universo."')
    add('Rodapé','"IBGE · base 2022 · " & [Cenário ativo] & " · Pontuação relativa; não é previsão de retorno."')
    add('Subtítulo','"Base 2022 · Cenário " & [Cenário ativo] & " · " & [Pesos ativos]')
    add('Unidades locais no ano','IF(HASONEVALUE(Municipio[id_municipio]), SUM(Historico[concorrentes]))','#,0')
    add('Valor contextual','IF(HASONEVALUE(Municipio[id_municipio]), SELECTEDVALUE(Contexto[valor]))')
    # Tabelas virtuais mantêm o texto alinhado ao cenário e à cidade real.
    factors='UNION('+','.join(f'ROW("Fator","{label}","Score",[{SCORE_NAMES[score]}],"Pontos",DIVIDE([{SCORE_NAMES[score]}]*[{weight}],[peso_mercado]+[peso_renda]+[peso_saturacao]+[peso_ocupacao]))' for label,score,weight in COMPONENTS)+')'
    verdict='VAR cidade=TOPN(1,FILTER(ALL(Municipio),CALCULATE(MAX(Fato2022[elegivel]))=1),[Índice],DESC,Municipio[id_municipio],ASC)\nVAR nome=CONCATENATEX(cidade,Municipio[municipio],"")\nVAR fatores=CALCULATETABLE('+factors+',cidade)\nVAR motivos=CONCATENATEX(TOPN(2,fatores,[Pontos],DESC,[Fator],ASC),[Fator] & " (" & FORMAT([Pontos],"0.0") & " pts)"," e ",[Pontos],DESC)\nVAR empates=COUNTROWS(FILTER(ALL(Municipio),CALCULATE(MAX(Fato2022[elegivel]))=1 && ABS([Índice]-[Índice do líder])<0.000000001))\nRETURN IF([Elegíveis]=0,"Sem base validada para recomendar",nome & " lidera " & [Cenário ativo] & " · 2022 · " & FORMAT([Índice do líder],"0.0") & "/100." & IF(empates>1," Empate no topo; ordem técnica por código IBGE.","") & UNICHAR(10) & "Maiores contribuições: " & motivos & "." & UNICHAR(10) & "Prioridade para estudo comercial; custos, logística e retorno financeiro não foram estimados.")'
    summary='VAR fatores='+factors+'\nVAR forte=CONCATENATEX(TOPN(1,fatores,[Score],DESC,[Fator],ASC),[Fator] & " (" & FORMAT([Score],"0.0") & "/100)","")\nVAR fraco=CONCATENATEX(TOPN(1,fatores,[Score],ASC,[Fator],ASC),[Fator] & " (" & FORMAT([Score],"0.0") & "/100)","")\nRETURN IF(NOT HASONEVALUE(Municipio[id_municipio]),"Selecione um município pelo nome para avaliar seus indicadores.",IF(MAX(Fato2022[elegivel])<>1,"Índice indisponível: componente ausente; ausência não é zero.",SELECTEDVALUE(Municipio[municipio]) & " · " & FORMAT([Índice],"0.0") & "/100 · " & [Cenário ativo] & UNICHAR(10) & "Ponto forte relativo: " & forte & "." & UNICHAR(10) & "Menor score relativo: " & fraco & ". Pontuação estadual; não estima retorno."))'
    result=[(n,verdict if n=='Veredito' else summary if n=='Resumo municipal' else e,f) for n,e,f in result]
    return result


def build_model(snapshot,values):
    dump(MODEL/'definition.pbism',{'$schema':SCHEMA+'item/semanticModel/definitionProperties/1.0.0/schema.json','version':'4.2','settings':{'qnaEnabled':False}})
    (MODEL/'definition').mkdir(parents=True,exist_ok=True)
    (MODEL/'definition/database.tmdl').write_text('database\n\tcompatibilityLevel: 1600\n',encoding='utf-8')
    names=['Municipio','Fato2022','Cenario','Componente','Sensibilidade','Contexto','Historico']
    (MODEL/'definition/model.tmdl').write_text('model Model\n\tculture: pt-BR\n\tdefaultPowerBIDataSourceVersion: powerBI_V3\n\tsourceQueryCulture: pt-BR\n\tdataAccessOptions\n\t\tlegacyRedirects\n\t\treturnErrorValuesAsNull\n\n'+''.join('ref table '+x+'\n' for x in names),encoding='utf-8')
    tmdl_table('Municipio',[('id_municipio','string',None),('municipio','string',None)],values)
    numeric=['populacao','domicilios','renda','ocupados','populacao_14mais','concorrentes','taxa_ocupacao','saturacao','score_domicilios','score_renda','score_saturacao','score_ocupacao']
    tmdl_table('Fato2022',[('id_municipio','string',None)]+[(x,'double','#,0.00') for x in numeric]+[('elegivel','int64','0')],values,measures())
    cs=[dict(zip(['cenario','peso_mercado','peso_renda','peso_saturacao','peso_ocupacao'],s)) for s in SCENARIOS]
    tmdl_table('Cenario',[('cenario','string',None)]+[(x,'int64','0') for x in ['peso_mercado','peso_renda','peso_saturacao','peso_ocupacao']],cs)
    tmdl_table('Componente',[('componente','string',None)],[{'componente':c[0]} for c in COMPONENTS])
    sensitivity=[]
    for scenario in SCENARIOS:
        scored=[(weighted_index([r[c[1]] for c in COMPONENTS],scenario[1:]),r) for r in values if r['elegivel']]
        scored.sort(key=lambda pair:(-pair[0],pair[1]['id_municipio']))
        for pos,(score,r) in enumerate(scored[:3],1):sensitivity.append({'cenario':scenario[0],'posicao':pos,'municipio':r['municipio'],'indice':score})
    tmdl_table('Sensibilidade',[('cenario','string',None),('posicao','int64','0'),('municipio','string',None),('indice','double','0.0')],sensitivity)
    context=[]
    labels={'renda':'Rendimento mediano mensal do trabalho','concorrentes':'Unidades locais varejistas CNAE 47.4','ocupados':'Pessoas ocupadas 14+'}
    for r in snapshot['linhas']:
        if r['kpi'] not in labels:continue
        context.append({'id_municipio':r['id_municipio'],'indicador':labels[r['kpi']],'periodo':str(r['periodo']),'valor': 'Não disponível' if r['valor'] is None else ('R$ ' if r['kpi']=='renda' else '')+format(r['valor'],',.0f').replace(',','.'),'unidade':r['unidade']})
    tmdl_table('Contexto',[(x,'string',None) for x in ['id_municipio','indicador','periodo','valor','unidade']],context)
    historical=[{'id_municipio':r['id_municipio'],'ano':r['periodo'],'concorrentes':r['valor']} for r in snapshot['linhas'] if r['kpi']=='concorrentes']
    tmdl_table('Historico',[('id_municipio','string',None),('ano','int64','0'),('concorrentes','double','#,0')],historical)
    relationships=''
    for table in ['Fato2022','Contexto','Historico']:
        relationships+=f'relationship {uuid.uuid5(uuid.NAMESPACE_DNS,"bi-sc-rel."+table)}\n\tfromColumn: {table}.id_municipio\n\ttoColumn: Municipio.id_municipio\n\n'
    (MODEL/'definition/relationships.tmdl').write_text(relationships,encoding='utf-8')
    dump(OUT/'resultados.json',{'fonte_sql':snapshot['fonte_sql'],'exportado_em':snapshot['exportado_em'],'elegiveis':sum(r['elegivel'] for r in values),'municipios':len(values),'cenarios':sensitivity,'ranking_equilibrado':sorted([dict(r,indice=weighted_index([r[c[1]] for c in COMPONENTS],SCENARIOS[0][1:])) for r in values if r['elegivel']],key=lambda r:(-r['indice'],r['id_municipio']))})


def literal(value):
    value= ('true' if value else 'false') if isinstance(value,bool) else str(value) if isinstance(value,(int,float)) else "'"+str(value).replace("'","''")+"'"
    return {'expr':{'Literal':{'Value':value}}}


def numeric(value,kind='D'):
    """Literais tipados usados pelo Desktop: D para contínuos, L para precisão."""
    if kind not in ('D','L') or isinstance(value,bool):raise ValueError('Literal numérico inválido')
    return {'expr':{'Literal':{'Value':str(value)+kind}}}


def color(value):return {'solid':{'color':literal(value)}}


def field(table,prop,measure=False):
    return {('Measure' if measure else 'Column'):{'Expression':{'SourceRef':{'Entity':table}},'Property':prop}}


def projection(table,prop,measure=False):
    return {'field':field(table,prop,measure),'queryRef':table+'.'+prop,'nativeQueryRef':prop}


def container_title(title):
    return {'title':[{'properties':{'show':literal(True),'text':literal(title),'fontColor':color('#392D25'),'fontFamily':literal('Segoe UI'),'fontSize':numeric(14),'alignment':literal('left')}}],
            'background':[{'properties':{'show':literal(True),'color':color('#FFFFFF'),'transparency':numeric(0)}}],
            'border':[{'properties':{'show':literal(True),'color':color('#E4DACD'),'radius':numeric(12)}}],
            'visualHeader':[{'properties':{'show':literal(False)}}]}


def visual(page,name,kind,x,y,w,h,title=None,roles=None,objects=None,hidden=False):
    v={'$schema':SCHEMA+'item/report/definition/visualContainer/2.5.0/schema.json','name':name,
       'position':{'x':x,'y':y,'z':1000,'height':h,'width':w,'tabOrder':1000},
       'visual':{'visualType':kind,'drillFilterOtherVisuals':True}}
    if title:v['visual']['visualContainerObjects']=container_title(title)
    if roles:v['visual']['query']={'queryState':{role:{'projections':projections} for role,projections in roles.items()}}
    if objects:v['visual']['objects']=objects
    if hidden:v['isHidden']=True
    path=REPORT/'definition/pages'/page/'visuals'/name/'visual.json'
    dump(path,v)
    return path,v


def card(page,name,measure,x,y,w,h,title,size=27):
    return visual(page,name,'card',x,y,w,h,title,{'Values':[projection('Fato2022',measure,True)]},
        {'labels':[{'properties':{'color':color('#392D25'),'fontSize':numeric(size),'fontFamily':literal('Segoe UI'),'labelDisplayUnits':numeric(1)}}],
         'wordWrap':[{'properties':{'show':literal(True)}}],
         'categoryLabels':[{'properties':{'show':literal(False)}}]})


def text(page,name,content,x,y,w,h,size=14):
    return visual(page,name,'textbox',x,y,w,h,objects={'general':[{'properties':{'paragraphs':[{'textRuns':[{'value':content,'textStyle':{'fontFamily':'Segoe UI','fontSize':str(size)+'pt','color':'#392D25'}}]}]}}]})


def slicer(page,name,table,col,x,y,w,h,title,sync=None,hidden=False,default=None,search=False):
    path,v=visual(page,name,'slicer',x,y,w,h,title,{'Values':[projection(table,col)]},
        {'data':[{'properties':{'mode':literal('Dropdown')}}],
         'selection':[{'properties':{'singleSelect':literal(True),'selectAllCheckboxEnabled':literal(False)}}],
         'items':[{'properties':{'fontColor':color('#392D25'),'textSize':numeric(12)}}],
         'header':[{'properties':{'show':literal(False)}}]},hidden)
    if sync:v['visual']['syncGroup']={'groupName':sync,'fieldChanges':True,'filterChanges':True}
    general={}
    if search:general['selfFilterEnabled']=literal(True)
    if default is not None:
        general['filter']={'filter':{'Version':2,'From':[{'Name':'t','Entity':table,'Type':0}],
            'Where':[{'Condition':{'In':{'Expressions':[{'Column':{'Expression':{'SourceRef':{'Source':'t'}},'Property':col}}],
                                        'Values':[[{'Literal':{'Value':"'"+default.replace("'","''")+"'"}}]]}}}]}}
    if general:v['visual']['objects']['general']=[{'properties':general}]
    dump(path,v)


def chart(page,name,kind,x,y,w,h,title,category,measure,table='Fato2022',axis_max=None):
    objects={'dataPoint':[{'properties':{'defaultColor':color('#B85016')}}],
             'legend':[{'properties':{'show':literal(False)}}],
             'categoryAxis':[{'properties':{'show':literal(True),'fontSize':numeric(12),'showAxisTitle':literal(False)}}],
             'valueAxis':[{'properties':{'show':literal(True),'start':numeric(0),'showAxisTitle':literal(False),'fontSize':numeric(12)}}],
             'labels':[{'properties':{'show':literal(True),'fontSize':numeric(12),'labelDisplayUnits':numeric(0),'labelPrecision':numeric(1,'L')}}]}
    if axis_max is not None:objects['valueAxis'][0]['properties']['end']=numeric(axis_max)
    path,v=visual(page,name,kind,x,y,w,h,title,{'Category':[projection(*category)],'Y':[projection(table,measure,True)]},objects)
    if kind=='barChart':v['visual']['query']['sortDefinition']={'sort':[{'field':field(table,measure,True),'direction':'Descending'}]}
    dump(path,v)


def build_report(snapshot):
    dump(OUT/'filial_construcao_sc.pbip',{'$schema':SCHEMA+'pbip/pbipProperties/1.0.0/schema.json','version':'1.0','artifacts':[{'report':{'path':'filial_construcao_sc.Report'}}],'settings':{'enableAutoRecovery':True}})
    dump(REPORT/'definition.pbir',{'$schema':SCHEMA+'item/report/definitionProperties/2.0.0/schema.json','version':'4.0','datasetReference':{'byPath':{'path':'../filial_construcao_sc.SemanticModel'}}})
    dump(REPORT/'definition/version.json',{'$schema':SCHEMA+'item/report/definition/versionMetadata/1.0.0/schema.json','version':'2.0.0'})
    theme={'name':'SC Bege e Laranja','dataColors':['#B85016','#F3CEAC','#685B50'],'background':'#F7F2E9','foreground':'#392D25','tableAccent':'#B85016','textClasses':{'label':{'fontFace':'Segoe UI','fontSize':12},'title':{'fontFace':'Segoe UI','fontSize':16}}}
    dump(REPORT/'StaticResources/RegisteredResources/tema_sc.json',theme)
    version={'visual':'2.5.0','report':'3.1.0','page':'2.0.0'}
    dump(REPORT/'definition/report.json',{'$schema':SCHEMA+'item/report/definition/report/3.1.0/schema.json',
       'themeCollection':{'baseTheme':{'name':'CY24SU02','reportVersionAtImport':version,'type':'SharedResources'},'customTheme':{'name':'tema_sc','reportVersionAtImport':version,'type':'RegisteredResources'}},
       'resourcePackages':[{'name':'RegisteredResources','type':'RegisteredResources','items':[{'name':'tema_sc','path':'tema_sc.json','type':'CustomTheme'}]}],
       'settings':{'useStylableVisualContainerHeader':True,'defaultFilterActionIsDataFilter':True,'useEnhancedTooltips':True}})
    pages=[('visao_geral','Visão Geral e Veredito'),('analise_municipio','Análise por Município')]
    dump(REPORT/'definition/pages/pages.json',{'$schema':SCHEMA+'item/report/definition/pagesMetadata/1.0.0/schema.json','pageOrder':[x[0] for x in pages],'activePageName':'visao_geral'})
    for page,title in pages:
        dump(REPORT/'definition/pages'/page/'page.json',{'$schema':SCHEMA+'item/report/definition/page/2.0.0/schema.json','name':page,'displayName':title,'displayOption':'FitToPage','height':900,'width':1600,
              'objects':{'background':[{'properties':{'color':color('#F7F2E9'),'transparency':numeric(0)}}]}})
        text(page,'titulo', 'Decisão de expansão · Santa Catarina' if page=='visao_geral' else 'Análise por município · Santa Catarina',32,24,1150,44,22)
        card(page,'subtitulo','Subtítulo',32,78,1536,24,None,11)
        visual(page,'navegacao','pageNavigator',1236,24,332,40,objects={'buttonText':[{'properties':{'fontSize':numeric(10)}}]})
        text(page,'rodape','IBGE · Base 2022 · Dados '+snapshot['fonte_sql'].split('fontes_')[-1]+' · Pontuação relativa; não estima retorno financeiro.',32,844,1536,36,11)
    p='visao_geral'
    for n,m,x,w,title,size in [('lider','Município líder',32,368,'Município líder',26),('indice','Índice do líder',424,368,'Índice do líder · 2022',29),('ano','Ano',816,368,'Ano de referência',29),('cobertura','Cobertura',1208,360,'Cobertura elegível',29)]:card(p,n,m,x,112,w,96,title,size)
    card(p,'veredito','Veredito',32,232,1536,82,None,12)
    chart(p,'ranking','barChart',32,338,920,482,'Top 10 · índice do cenário ativo · 2022',('Municipio','municipio'),'Índice Top 10',axis_max=100)
    slicer(p,'cenario','Cenario','cenario',976,338,592,110,'Cenário de pesos · seleção única','cenario',default='Referência')
    visual(p,'sensibilidade','tableEx',976,472,592,348,'Sensibilidade · top 3 em cada cenário',{'Values':[projection('Sensibilidade',c) for c in ['cenario','posicao','municipio','indice']]},
           {'grid':[{'properties':{'textSize':numeric(12),'gridVertical':literal(False)}}],'columnHeaders':[{'properties':{'fontColor':color('#392D25'),'fontSize':numeric(12)}}]})
    pagepath=REPORT/'definition/pages'/p/'page.json'
    pg=json.loads(pagepath.read_text(encoding='utf-8'))
    pg['visualInteractions']=[{'source':'ranking','target':target,'type':'NoFilter'} for target in ['lider','indice','ano','cobertura','veredito','cenario','sensibilidade']]
    dump(pagepath,pg)
    p='analise_municipio'
    lider=json.loads((OUT/'resultados.json').read_text(encoding='utf-8'))['ranking_equilibrado'][0]['municipio']
    slicer(p,'municipio','Municipio','municipio',32,112,520,88,'Município · selecione pelo nome',default=lider,search=True)
    card(p,'resumo','Resumo municipal',576,112,992,88,None,13)
    for n,m,x,w,title in [('indice','Índice municipal',32,368,'Índice · cenário ativo · 2022'),('posicao','Posição estadual',424,368,'Posição estadual · 2022'),('populacao','População residente',816,368,'População residente · 2022'),('domicilios','Domicílios ocupados',1208,360,'Domicílios ocupados · 2022')]:card(p,n,m,x,224,w,96,title,26)
    chart(p,'componentes','barChart',32,344,744,476,'Contribuição ao índice · pontos · 2022',('Componente','componente'),'Contribuição',axis_max=100)
    chart(p,'historico','lineChart',800,344,768,240,'Unidades locais varejistas CNAE 47.4 · 2022–24',('Historico','ano'),'Unidades locais no ano')
    visual(p,'contexto','tableEx',800,608,768,212,'Contexto · unidade e ano explícitos',{'Values':[projection('Contexto','indicador'),projection('Contexto','periodo'),projection('Fato2022','Valor contextual',True),projection('Contexto','unidade')]}, {'grid':[{'properties':{'textSize':numeric(11),'gridVertical':literal(False)}}]})
    slicer(p,'cenario_sincronizado','Cenario','cenario',0,0,1,1,'Cenário','cenario',hidden=True,default='Referência')


def verify_structure():
    pages=list((REPORT/'definition/pages').glob('*/page.json'))
    if len(pages)!=2:raise ValueError('Exatamente duas páginas exigidas')
    names=set()
    for f in REPORT.rglob('visual.json'):
        v=json.loads(f.read_text(encoding='utf-8'))
        key=(f.parents[2].name,v['name'])
        if key in names:raise ValueError('Visual duplicado')
        names.add(key)
        if not v.get('isHidden'):
            p=v['position']
            if p['x']<0 or p['y']<0 or p['x']+p['width']>1600 or p['y']+p['height']>900:raise ValueError('Visual fora da página')
    return {'paginas':len(pages),'visuais':len(names)}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--source',help='Snapshot versionado SQL, exemplo bi_validado.fontes_<UTC>')
    args=parser.parse_args()
    snapshot=export_sql(args.source) if args.source else json.loads((OUT/'dados_snapshot.json').read_text(encoding='utf-8'))
    values=pivot(snapshot)
    build_model(snapshot,values)
    build_report(snapshot)
    print(json.dumps(verify_structure(),ensure_ascii=False))
