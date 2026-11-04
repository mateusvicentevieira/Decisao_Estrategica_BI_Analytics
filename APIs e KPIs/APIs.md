# Fontes oficiais e APIs — versão corrigida

Atualizado em 04/11/2026. Esta documentação descreve as fontes efetivamente usadas pelo coletor corrigido e pelo índice. As consultas e definições antigas foram substituídas; não reutilizar seus valores ou scores no modelo atual.

## Coleta e rastreabilidade

O coletor [ETLs/corrigido/coletor.py](../ETLs/corrigido/coletor.py) consulta municípios de Santa Catarina por código IBGE e grava dados em versões independentes de `bi_validado`, preservando as tabelas anteriores. A versão usada no relatório é `bi_validado.fontes_20261103_135300`: oito séries × 295 municípios, total de 2.360 registros. Respostas oficiais, metadados, valores brutos, URLs e hashes SHA-256 são preservados por execução.

O [cadastro municipal oficial](https://servicodados.ibge.gov.br/api/v1/localidades/estados/42/municipios) define os 295 municípios esperados. Nas consultas de agregados, `localidades=N6[N3[42]]` seleciona o nível municipal de SC.

## Fontes utilizadas

| Série | Ano | Agregado / variável | Unidade e universo |
|---|---|---|---|
| População residente | 2022 | 4709 / 93 | Pessoas; população residente total. |
| Domicílios | 2022 | 4712 / 381 | Domicílios particulares permanentes ocupados. |
| Rendimento mediano | 2022 | 10289 / 13537 | Reais; rendimento nominal mediano mensal de todos os trabalhos dos ocupados de 14 anos ou mais com rendimento de trabalho. |
| Ocupados 14+ | 2022 | 10268 / 696 | Pessoas de 14 anos ou mais ocupadas na semana de referência. |
| População 14+ | 2022 | 10268 / 140 | Pessoas de 14 anos ou mais; denominador no mesmo universo dos ocupados. |
| Unidades locais CNAE 47.4 | 2022, 2023 e 2024 | 9528 / 706 | Unidades locais do comércio varejista de material de construção, grupo 47.4. |

Endpoints exatos em termos de seleção, com caracteres de consulta codificados nos links:

- [População residente 2022](https://servicodados.ibge.gov.br/api/v3/agregados/4709/periodos/2022/variaveis/93?localidades=N6%5BN3%5B42%5D%5D). Sem classificação adicional. [Metadados 4709](https://servicodados.ibge.gov.br/api/v3/agregados/4709/metadados).
- [Domicílios ocupados 2022](https://servicodados.ibge.gov.br/api/v3/agregados/4712/periodos/2022/variaveis/381?localidades=N6%5BN3%5B42%5D%5D). Sem classificação adicional. [Metadados 4712](https://servicodados.ibge.gov.br/api/v3/agregados/4712/metadados).
- [Rendimento mediano 2022](https://servicodados.ibge.gov.br/api/v3/agregados/10289/periodos/2022/variaveis/13537?localidades=N6%5BN3%5B42%5D%5D&classificacao=2%5B6794%5D%7C86%5B95251%5D). Classificação `2[6794]|86[95251]`. [Metadados 10289](https://servicodados.ibge.gov.br/api/v3/agregados/10289/metadados).
- [Ocupados 14+ em 2022](https://servicodados.ibge.gov.br/api/v3/agregados/10268/periodos/2022/variaveis/696?localidades=N6%5BN3%5B42%5D%5D&classificacao=2%5B6794%5D%7C86%5B95251%5D%7C58%5B82072%5D) e [população 14+ em 2022](https://servicodados.ibge.gov.br/api/v3/agregados/10268/periodos/2022/variaveis/140?localidades=N6%5BN3%5B42%5D%5D&classificacao=2%5B6794%5D%7C86%5B95251%5D%7C58%5B82072%5D). Mesmas classificações `2[6794]|86[95251]|58[82072]`; categoria 82072 restringe a 14 anos ou mais. O nome geral das variáveis menciona 10 anos ou mais, mas a categoria selecionada define o universo efetivo. [Metadados 10268](https://servicodados.ibge.gov.br/api/v3/agregados/10268/metadados).
- Unidades locais varejistas: [2022](https://servicodados.ibge.gov.br/api/v3/agregados/9528/periodos/2022/variaveis/706?localidades=N6%5BN3%5B42%5D%5D&classificacao=12762%5B117452%5D), [2023](https://servicodados.ibge.gov.br/api/v3/agregados/9528/periodos/2023/variaveis/706?localidades=N6%5BN3%5B42%5D%5D&classificacao=12762%5B117452%5D) e [2024](https://servicodados.ibge.gov.br/api/v3/agregados/9528/periodos/2024/variaveis/706?localidades=N6%5BN3%5B42%5D%5D&classificacao=12762%5B117452%5D). Classificação `12762[117452]`: grupo CNAE 47.4, consultado uma única vez sem somar classes filhas. [Metadados 9528](https://servicodados.ibge.gov.br/api/v3/agregados/9528/metadados).

## Índice e períodos

O índice combina somente 2022: 40% score de domicílios ocupados + 30% score de rendimento + 20% score inverso de saturação + 10% score de ocupação 14+. A saturação é `10.000 × unidades locais / população residente`; a taxa de ocupação é `100 × ocupados 14+ / população 14+`. Numeradores e denominadores pertencem a 2022 e a universos compatíveis.

O min–max usa limites fixos dos 295 municípios da versão. Sem variação ou componente ausente, não se atribui score arbitrário nem se redistribuem pesos. Os pesos são hipóteses gerenciais, sem calibração por retorno financeiro.

| Cenário | Domicílios | Rendimento | Saturação invertida | Ocupação 14+ |
|---|---:|---:|---:|---:|
| Referência | 40% | 30% | 20% | 10% |
| Pesos iguais | 25% | 25% | 25% | 25% |
| Ênfase mercado | 50% | 25% | 15% | 10% |
| Menor saturação | 30% | 25% | 35% | 10% |

As quantidades de unidades locais de 2022–2024 formam histórico separado. Não se usa população de 2022 como denominador em 2023/2024. A série CEMPRE iniciada em 2022 não é concatenada à série antiga encerrada em 2021.

## Qualidade e fontes excluídas

O marcador oficial `-` significa zero absoluto publicado e é convertido em zero com preservação do bruto. `X`, `..` e `...` ficam nulos. Ausência não é imputada. O coletor confere cobertura e chaves municipais antes da carga.

As fontes antigas de moradores 6750/9598 e domicílios 2022 10053/9599 cobrem recortes da Pesquisa Urbanística do Entorno, não totais municipais. O histórico antigo de domicílios, a soma sobreposta de categorias do CEMPRE, a proporção ativa/dependência anterior e o CAGED geral não entram no índice. Motivos em [KPIs de crescimento](KPIs_Crescimento.md) e no [diagnóstico](../docs/diagnostico_inicial.md).

O Power BI incorpora um snapshot público exportado exclusivamente do SQL corrigido; não atualiza automaticamente a partir da API ou do banco. Consulte o [README](../README.md) para atualizar e a [metodologia](../docs/metodologia.md) para limites, fórmulas e regras de empate. O índice expressa atratividade relativa, sem estimar ROI ou probabilidade de retorno.
