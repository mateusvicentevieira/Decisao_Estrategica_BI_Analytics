"""Validação declarada ou compatibilidade pública explícita, sem editar o projeto.

O Desktop pode salvar versões de schema ainda não publicadas. Nesses casos,
somente os mapeamentos explícitos abaixo são permitidos; o conteúdo inteiro
é validado em memória e a diferença é registrada. --strict-declared não usa
substitutos e mantém a falha de disponibilidade do schema nativo.
"""
from pathlib import Path
import argparse
import hashlib
import json
import sys
import warnings
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'.tools/python'))
import requests
import jsonschema
warnings.filterwarnings('ignore',category=DeprecationWarning)
CACHE=ROOT/'.tools/schemas'
PREFIX='https://developer.microsoft.com/json-schemas/fabric/'
COMPATIBILITY={
    PREFIX+'item/report/definition/visualContainer/2.14.0/schema.json':PREFIX+'item/report/definition/visualContainer/2.5.0/schema.json',
    PREFIX+'item/report/definition/report/3.3.0/schema.json':PREFIX+'item/report/definition/report/3.1.0/schema.json',
    PREFIX+'item/report/definition/pagesMetadata/1.1.0/schema.json':PREFIX+'item/report/definition/pagesMetadata/1.0.0/schema.json',
}
FORMAT_SCHEMAS={
    '.pbip':PREFIX+'pbip/pbipProperties/1.0.0/schema.json',
    '.pbir':PREFIX+'item/report/definitionProperties/2.0.0/schema.json',
    '.pbism':PREFIX+'item/semanticModel/definitionProperties/1.0.0/schema.json',
}
UNAVAILABLE={}

def validate_document(document,loader,allow_compatibility=True):
    declared=document['$schema'];effective=declared;mode='declared'
    try:
        schema=loader(declared)
    except requests.HTTPError as error:
        if not (error.response is not None and error.response.status_code==404 and
                allow_compatibility and declared in COMPATIBILITY):
            raise
        effective=COMPATIBILITY[declared]
        schema=loader(effective)
        mode='compatibility'
    candidate=dict(document)
    candidate['$schema']=effective
    resolver=jsonschema.RefResolver(base_uri=effective,referrer=schema,handlers={'https':loader})
    errors=[{'caminho':list(e.absolute_path),'mensagem':e.message} for e in jsonschema.Draft7Validator(schema,resolver=resolver).iter_errors(candidate)]
    return {'mode':mode,'errors':errors,'declared_schema':declared,'validated_schema':effective}

def fetch(url):
    if url in UNAVAILABLE:raise UNAVAILABLE[url]
    CACHE.mkdir(parents=True,exist_ok=True)
    path=CACHE/(hashlib.sha256(url.encode()).hexdigest()+'.json')
    if path.exists():return json.loads(path.read_text(encoding='utf-8'))
    source=url.replace('https://developer.microsoft.com/json-schemas/','https://raw.githubusercontent.com/microsoft/json-schemas/main/').replace('schema.embedded.json','schema-embedded.json')
    response=requests.get(source,timeout=60)
    try:
        response.raise_for_status()
    except requests.HTTPError as error:
        if response.status_code==404:UNAVAILABLE[url]=error
        raise
    schema=response.json()
    path.write_text(json.dumps(schema),encoding='utf-8')
    return schema

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--strict-declared',action='store_true',help='Não utilizar versões públicas substitutas para schemas declarados indisponíveis')
    parser.add_argument('--report',type=Path,help='Salvar evidência JSON fora dos arquivos do projeto')
    args=parser.parse_args()
    counts={'schema_declarado':0,'compatibilidade_publica':0,'schema_publico_por_extensao':0}
    failures=[];compatibility=[];without_schema=[];inferred=[]
    for path in sorted((ROOT/'dashboard').rglob('*')):
        if '.pbi' in path.parts:continue
        if path.suffix not in ('.json','.pbip','.pbir','.pbism'):continue
        relative=str(path.relative_to(ROOT)).replace('\\','/')
        document=json.loads(path.read_text(encoding='utf-8'))
        from_extension=False
        if '$schema' not in document:
            if path.suffix not in FORMAT_SCHEMAS:
                without_schema.append(relative)
                continue
            document=dict(document,**{'$schema':FORMAT_SCHEMAS[path.suffix]})
            from_extension=True
        try:
            result=validate_document(document,fetch,allow_compatibility=not args.strict_declared)
            if result['errors']:
                failures.append({'arquivo':relative,'schema_validacao':result['validated_schema'],'erros':result['errors']})
                continue
            if from_extension:
                counts['schema_publico_por_extensao']+=1
                inferred.append({'arquivo':relative,'schema_validacao':result['validated_schema']})
            elif result['mode']=='compatibility':
                counts['compatibilidade_publica']+=1
                compatibility.append({'arquivo':relative,'schema_declarado':result['declared_schema'],'schema_validacao':result['validated_schema']})
            else:counts['schema_declarado']+=1
        except Exception as error:
            failures.append({'arquivo':relative,'schema_declarado':document['$schema'],'erro_disponibilidade_ou_execucao':str(error)})
    report={'data':'2026-11-04','modo':'estrito_declarado' if args.strict_declared else 'compatibilidade_explicita',
            'arquivos_validados':sum(counts.values()),'contagens':counts,
            'compatibilidade_somente_em_memoria':compatibility,'schemas_inferidos_por_extensao':inferred,
            'arquivos_sem_schema_nao_validados':without_schema,'falhas':failures,
            'observacao':'Compatibilidade pública não comprova o schema nativo indisponível. Nenhum arquivo do projeto é alterado; nenhuma propriedade é removida para validar.'}
    if args.report:
        args.report.parent.mkdir(parents=True,exist_ok=True)
        args.report.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    sys.exit(bool(failures))
