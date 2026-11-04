# Diagnóstico inicial — seleção de município para filial em SC

Data: 3 de novembro de 2026. Registro histórico do diagnóstico inicial; não constitui entrega final, ranking ou recomendação de município. A primeira revisão crítica foi concluída com decisão **Ajustes**. A retomada autorizada e as correções posteriores constam abaixo e em [briefing e checkpoints](briefing_e_checkpoints.md).

## Briefing e autorizações

O projeto deve comparar os municípios de Santa Catarina para apoiar a escolha de uma filial varejista de materiais de construção. A entrega prevista é um projeto compatível com Power BI Desktop, com exatamente duas páginas: visão geral com ranking e veredito; análise individual com segmentador por nome do município.

O usuário autorizou consultar todas as tabelas do PostgreSQL e editar somente `normalizacao`. Os dados devem ser tratados como brutos, sem filtros empresariais prévios. A escolha dos KPIs foi delegada à equipe, considerando os arquivos de `APIs e KPIs`. A preferência visual é por bege e laranja, com fundo minimalista inspirado nas imagens fornecidas.

Todos os anos disponíveis podem ser analisados. Razões, índices e demais fórmulas que combinam indicadores devem usar componentes do mesmo período. Comparações históricas exigem conceitos e universos compatíveis; não se deve misturar anos entre numerador e denominador de uma taxa de nível. Uma variação histórica deve identificar explicitamente seus dois períodos e só ser calculada depois de validada a comparabilidade.

## Fontes e ambiente conferidos

- O PostgreSQL está acessível. A exploração desta etapa utilizou consultas em transação somente leitura.
- O banco atual contém nove tabelas, incluindo `normalizacao` e `populacao_ocupada_municipio`. As fontes cobrem 295 municípios, salvo o CAGED, com 294.
- O backup `DecisaoEstrategica_20261103_081612.backup`, com 94.315 bytes, foi reconhecido por `pg_restore --list` como formato CUSTOM/PGDMP, PostgreSQL 18.4, criado em 03/11/2026 às 08:16. Seu inventário contém oito tabelas e não inclui `populacao_ocupada_municipio`. Não houve restauração.
- `arquivo.sql` contém apenas `SELECT * FROM normalizacao;`; não é o backup completo.
- O Power BI Desktop está instalado. Sua presença não comprova a abertura de um projeto ainda não produzido.

## Achados e impacto nos KPIs

| Item | Evidência apurada | Consequência e correção necessária |
|---|---|---|
| Moradores de 2022 | O agregado 6750, variável 9598, utiliza recorte de setores da Pesquisa Urbanística do Entorno. | Não representa o total populacional municipal. Obter uma fonte municipal com universo apropriado antes de pontuar mercado ou usá-la como denominador. |
| Domicílios de 2022 e série histórica | O agregado 10053, variável 9599, também se refere ao recorte do entorno. O universo difere da série histórica utilizada. Em 203 dos 295 municípios o valor de 2022 é inferior ao de 2010. | A diferença não comprova queda no número de domicílios. Bloquear crescimento entre essas séries até obter universos comparáveis. |
| Empresas/CEMPRE | A soma combina seção F com divisão 41; grupo 46.7 com suas cinco classes; grupo 47.4 com suas quatro classes. Há sobreposição hierárquica e mistura de construção, atacado e varejo. | O total não pode ser interpretado como empresas únicas ou concorrentes. Selecionar categorias mutuamente exclusivas e definir a cobertura de concorrência antes de normalizar. |
| Idade ativa, dependência e ocupação | A população ativa corresponde a 15–69 anos; dependentes, a 0–14 e 70 anos ou mais; ocupados, a 14 anos ou mais. | A taxa de ocupação proposta possui universos etários incompatíveis. Harmonizar as faixas antes da divisão. A razão de dependência com esse corte deve ser identificada explicitamente e ter sua utilização validada. |
| Rendimento mediano | Mediana mensal nominal dos rendimentos de todos os trabalhos das pessoas ocupadas de 14 anos ou mais com rendimento. | Pode contextualizar rendimentos do trabalho, mas não deve ser rotulada como renda domiciliar per capita ou renda de toda a população. |
| CAGED | Dados de janeiro a agosto de 2026. O processo de carga filtra SC, sem comprovação de filtro CNAE de construção civil. | Tratar como emprego formal geral no período observado; não como obras, emprego da construção ou acumulado de 12 meses. Para o KPI setorial, corrigir o recorte e conferir a cobertura mensal. |
| Normalização existente | O snapshot não é elegível para ranking e ainda descreve população ocupada como indisponível, embora ela exista no banco atual. | Atualizar a documentação e o snapshot somente depois da validação conceitual das fontes. A presença da nova tabela não resolve, por si só, a incompatibilidade etária. |

## Encaminhamento recomendado

Na primeira etapa, foi recomendado corrigir os processos de coleta e tratamento e recarregar as fontes necessárias para um ranking de atratividade. Isso exigiu ampliar a autorização inicial, que se limitava a editar `normalizacao`.

**Retomada autorizada:** o usuário autorizou expressamente correções e nova coleta, preservando os dados existentes. O coletor separado `ETLs/corrigido/coletor.py` passou a obter as fontes oficiais adequadas e gravar versões independentes no schema `bi_validado`; as tabelas originais de `public` permanecem preservadas. O diagnóstico da tabela anterior descreve as origens antigas e não deve ser atribuído automaticamente à nova camada.

As novas fontes usam população residente total `4709/93`, domicílios particulares permanentes ocupados `4712/381`, rendimento `10289/13537`, ocupados e população de 14 anos ou mais no mesmo agregado `10268` e unidades locais do grupo CNAE 47.4 no CEMPRE `9528/706`, sem somar categorias filhas. O índice utiliza apenas 2022; a concorrência de 2023 e 2024 fica em histórico separado. Detalhes em [metodologia](metodologia.md).

O tratamento do marcador oficial `-` foi corrigido para zero absoluto publicado, preservando o bruto. `X`, `..` e `...` permanecem sem valor. Isso difere de imputar zero a uma ausência. O histórico incompatível de domicílios e o CAGED geral permanecem fora do índice.

Um índice limitado a rendimento e população ocupada de 2022 teria alcance restrito ao mercado de trabalho e não resolveria a seleção de município para expansão varejista. Esse substituto não foi adotado. Os resultados do índice corrigido devem ser consultados no relatório, depois de validados; não há cálculo de probabilidade de retorno ou ROI.

Antes de compor o índice, a equipe deve validar os conceitos, períodos, cobertura, categorias exclusivas e ausências; justificar os pesos; e avaliar a sensibilidade do resultado. Ausência não deve ser convertida automaticamente em zero.

## Revisão crítica e decisão do Gerente

O Crítico concluiu a revisão com seis pendências de severidade alta: universo de moradores e domicílios; comparabilidade histórica e tratamento de zeros; dupla contagem e conceito de concorrência; universos da taxa de ocupação; CAGED sem recorte setorial; e combinação de períodos incompatíveis. Também registrou uma pendência média sobre atualização do snapshot e proveniência.

Decisão inicial do Gerente: **Ajustes**. Foi apresentada ao usuário a escolha entre autorizar correções dos ETLs e das fontes, com preservação dos dados existentes, ou seguir com uma análise descritiva provisória. O usuário autorizou a primeira opção. A liberação final depende da revalidação das correções pelo Crítico, da verificação do relatório no Power BI e do checkpoint do Gerente. A primeira revisão já foi concluída; a revalidação verifica os novos dados e a implementação. O estado atualizado consta em [briefing e checkpoints](briefing_e_checkpoints.md).

## Referências para auditoria

As definições e classificações foram conferidas pelo Analista nos metadados oficiais do IBGE e confrontadas com os arquivos de `APIs e KPIs` e os ETLs locais:

- [Agregado 6750 — metadados](https://servicodados.ibge.gov.br/api/v3/agregados/6750/metadados).
- [Agregado 10053 — metadados](https://servicodados.ibge.gov.br/api/v3/agregados/10053/metadados).
- [Agregado 206 — metadados da série histórica de domicílios](https://servicodados.ibge.gov.br/api/v3/agregados/206/metadados).
- [Agregado 6450 — metadados e classificações do CEMPRE](https://servicodados.ibge.gov.br/api/v3/agregados/6450/metadados).
- [Agregado 6893 — metadados e faixas etárias](https://servicodados.ibge.gov.br/api/v3/agregados/6893/metadados).
- [Agregado 10289 — metadados de rendimento](https://servicodados.ibge.gov.br/api/v3/agregados/10289/metadados).
- [Agregado 10268 — metadados da população ocupada](https://servicodados.ibge.gov.br/api/v3/agregados/10268/metadados).

Nenhuma credencial, string de conexão ou dado sensível foi incluído neste documento.
