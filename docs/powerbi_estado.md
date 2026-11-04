# Estado da montagem Power BI

Implementação em 03/11/2026; verificação final em 04/11/2026. A pesquisa inicial foi interrompida e retomada após autorização do usuário. O projeto foi gerado e aberto no Power BI Desktop pelo Gerente. Esta nota registra a implementação e seus testes; o aceite final consta no checkpoint do Gerente.

## Decisões confirmadas pelo Gerente

- Entrega: PBIP com modelo TMDL e relatório PBIR, exatamente duas páginas nativas.
- Dados de abertura: snapshot público exportado exclusivamente de `bi_validado.fontes_20261103_135300`, incorporado por Power Query `#table` para abrir sem credenciais. O script de atualização reproduz a exportação SQL usando variáveis de ambiente locais; nenhum host, banco ou credencial real foi incorporado no projeto versionável.
- Índice com componentes somente de 2022: domicílios ocupados (porte), rendimento mediano do trabalho, concorrência por 10 mil habitantes invertida e ocupação de 14 anos ou mais. Pesos de referência: 40/30/20/10, aprovados como hipótese explícita, sem calibração de retorno financeiro.
- Quatro cenários: Referência 40/30/20/10; Pesos iguais 25/25/25/25; Ênfase mercado 50/25/15/10; Menor saturação 30/25/35/10. Os pesos não são estimativa de ROI.
- População não recebe peso adicional ao de domicílios, evitando dupla pontuação de porte.
- Aparência conforme `design_dashboard.md`: bege/laranja, tela 1600×900, duas páginas e gráficos nativos. Histórico aprovado: unidades locais varejistas CNAE 47.4 de 2022 a 2024, sem usar a série incompatível de domicílios.

## Contrato esperado das fontes

O Analista informou viabilidade dos agregados oficiais: população2022 `4709/93`; domicílios particulares permanentes ocupados2022 `4712/381`; população14+ e ocupados14+ `10268/140` e `10268/696`, categoria `82072`; rendimento2022 `10289/13537`; CEMPRE2022 `9528`, grupo varejista47.4 categoria `117452`, sem somar categorias descendentes. Nenhuma dessas fontes foi exportada ou novamente validada por este agente.

O contrato final foi entregue pelo Analista e exportado do PostgreSQL em transação somente leitura: 2.360 linhas, oito séries com 295 municípios cada. Os marcadores `-` de concorrência foram interpretados pelo coletor como zero absoluto publicado, após conferência da legenda oficial do SIDRA. A versão inicial da coleta foi substituída sem alterar as tabelas públicas originais.

## Formato confirmado em fontes oficiais

Estrutura prevista:

```text
dashboard/
  filial_construcao_sc.pbip
  filial_construcao_sc.SemanticModel/
    definition.pbism
    definition/database.tmdl
    definition/model.tmdl
    definition/relationships.tmdl
    definition/tables/*.tmdl
  filial_construcao_sc.Report/
    definition.pbir
    definition/version.json
    definition/report.json
    definition/pages/pages.json
    definition/pages/<id>/page.json
    definition/pages/<id>/visuals/<id>/visual.json
```

- `.pbip`: esquema `fabric/pbip/pbipProperties/1.0.0/schema.json`, versão `1.0`, referência ao diretório `.Report`.
- `definition.pbism`: esquema `fabric/item/semanticModel/definitionProperties/1.0.0/schema.json`, versão `4.2`.
- `definition.pbir`: esquema `fabric/item/report/definitionProperties/2.0.0/schema.json`, versão `4.0`, referência relativa `byPath` ao diretório `.SemanticModel`.
- PBIR: arquivos `report/3.1.0`, `page/2.0.0`, `visualContainer/2.5.0` foram conferidos nos schemas públicos. O formato usa `visual.query.queryState`, projeções `Column`/`Measure` e referências `SourceRef.Entity`.
- O relatório contém `themeCollection`; as páginas contêm `name`, `displayName`, `displayOption` e esquema. O Desktop atualiza os schemas PBIR ao salvar; o gerador usa versões públicas que foram aceitas na abertura real.

Fontes: [estrutura PBIR Microsoft](https://learn.microsoft.com/en-us/rest/api/fabric/articles/item-management/definitions/report-definition), [referência PBIP mantida pela Microsoft](https://github.com/microsoft/skills-for-fabric/blob/main/skills/semantic-model-authoring/references/pbip.md), [schemas públicos Microsoft](https://github.com/microsoft/json-schemas/tree/main/fabric/item/report).

## Ambiente e próximos passos

Python disponível: `C:\Python314\python.exe`. `requests` disponível. A biblioteca `jsonschema` foi instalada localmente em `.tools/python` para validar os JSON pelos schemas oficiais; esse diretório e `.pbi` estão ignorados pelo Git.

Foram criados `scripts/build_dashboard.py`, `scripts/test_dashboard.py`, `scripts/validate_pbip.py`, `sql/views_kpis.sql`, `.env.example`, o snapshot público SQL e o projeto completo em `dashboard/filial_construcao_sc.pbip`. O modelo possui sete tabelas, com dimensão municipal, fatos de 2022, contexto/histórico e tabelas desconectadas de cenários, componentes e sensibilidade. São duas páginas e 26 visuais, incluindo um segmentador sincronizado oculto na segunda página, sem página adicional.

Verificações executadas: nove testes de comportamento/integridade do dashboard passaram; quatro testes adicionais verificam o tratamento honesto de esquemas indisponíveis, totalizando 13 testes aprovados em `scripts`. O Gerente confirmou no Desktop abertura, atualização, ranking top 10, eixo 0–100, filtro por nome, cenários sincronizados, texto completo e contribuições coerentes. Em Pesos iguais, Florianópolis apresentou 84,0 pontos e contribuições arredondadas de 25,0/24,7/17,1/17,1. A série de unidades locais da cidade exibiu 697/727/747.

A validação estrutural final está registrada em `validacao_estrutura.json`, com data de 04/11/2026: 21 arquivos passaram no esquema declarado; dez visuais salvos pelo Desktop com declaração `visualContainer/2.14.0` passaram integralmente por compatibilidade com o esquema público `2.5.0`; três descritores sem declaração passaram no esquema público identificado pela extensão. Total: 34 arquivos validados nesses três modos, sem falhas estruturais. Quatro JSON auxiliares sem esquema declarado não foram validados por JSON Schema: dados públicos, resultados, tema e diagrama.

O esquema `2.14.0` não estava publicado no endereço consultado. A compatibilidade foi verificada apenas em cópias em memória, substituindo somente a declaração `$schema` para atender ao identificador constante do esquema público. Todas as propriedades e valores originais foram submetidos à validação, sem remoção ou conversão de campos. Os arquivos nativos do projeto foram preservados. Isso **não comprova conformidade ao esquema nativo 2.14.0 indisponível**. O modo `--strict-declared` do verificador conserva a falha nesse caso; versões desconhecidas não recebem substituição automática.

Problemas detectados no Desktop foram corrigidos: variável DAX reservada `id` foi renomeada; literais de formatação passaram a usar tipo explícito (`12D`, por exemplo), evitando fonte padrão de 45 pontos; o enum nativo `labelDisplayUnits=1D` aplica números completos nos cartões, enquanto `0D` significa automático. O projeto foi salvo no Desktop com página inicial Visão Geral, cenário Referência e Florianópolis selecionada na análise individual. O Gerente confirmou leitura dos textos, eixo 0–100 e funcionamento dos filtros. Não houve interação deste agente com a interface do Power BI.
