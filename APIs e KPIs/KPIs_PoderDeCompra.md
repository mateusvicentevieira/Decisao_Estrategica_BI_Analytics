# KPIs — Rendimento e ocupação

Atualizado em 04/11/2026. Os indicadores abaixo integram o índice com fontes corrigidas de 2022. O título histórico da pasta “Poder de Compra” não transforma rendimento nominal do trabalho em renda disponível ou poder de compra atual.

## Rendimento nominal mediano mensal do trabalho

Fonte: [IBGE, agregado 10289, variável 13537, 2022](https://servicodados.ibge.gov.br/api/v3/agregados/10289/periodos/2022/variaveis/13537?localidades=N6%5BN3%5B42%5D%5D&classificacao=2%5B6794%5D%7C86%5B95251%5D). Classificações `2[6794]|86[95251]`.

Universo: pessoas de 14 anos ou mais ocupadas na semana de referência, **com rendimento de trabalho**. Mede o valor nominal mediano mensal de todos os trabalhos, em reais de 2022. A mediana divide a distribuição desse rendimento em duas partes; não é a média, nem renda domiciliar per capita, nem renda de toda a população.

O valor oficial recebe score min–max direto: `100 × (rendimento − mínimo estadual) / (máximo estadual − mínimo estadual)`.

**Peso de referência: 30% do índice total.** Maior rendimento recebe maior score por hipótese de capacidade econômica associada ao trabalho; não há validação causal de vendas de materiais de construção.

## Taxa de ocupação de pessoas de 14 anos ou mais

Fonte comum: IBGE, agregado 10268, 2022. Numerador: [variável 696, ocupados](https://servicodados.ibge.gov.br/api/v3/agregados/10268/periodos/2022/variaveis/696?localidades=N6%5BN3%5B42%5D%5D&classificacao=2%5B6794%5D%7C86%5B95251%5D%7C58%5B82072%5D). Denominador: [variável 140, população](https://servicodados.ibge.gov.br/api/v3/agregados/10268/periodos/2022/variaveis/140?localidades=N6%5BN3%5B42%5D%5D&classificacao=2%5B6794%5D%7C86%5B95251%5D%7C58%5B82072%5D).

Ambos usam as mesmas classificações `2[6794]|86[95251]|58[82072]`. A categoria etária 82072 restringe o universo efetivo a **14 anos ou mais**, embora o nome geral das variáveis mencione 10 anos ou mais.

```text
Taxa de ocupação 14+ (%) = 100 × ocupados 14+ de 2022 / população 14+ de 2022
Score = 100 × (taxa − mínimo estadual) / (máximo estadual − mínimo estadual)
```

**Peso de referência: 10% do índice total.** Representa a proporção ocupada no grupo etário, sem restringir a vínculos CLT. Não mede taxa de formalização, não usa admissões CAGED como estoque de ocupados e não divide ocupados 14+ pela antiga população de 15–69 anos.

## Indicadores anteriores excluídos

A proporção de população em idade ativa não integra o índice. O numerador antigo de 15–69 anos e os moradores do recorte de entorno não formam uma taxa municipal válida. A razão de dependência anterior também não recebe peso: é contexto demográfico com corte próprio, sem papel validado na decisão de expansão.

O emprego formal geral de janeiro a agosto de 2026 não é combinado com essas fontes de 2022. Nenhuma fórmula utiliza períodos ou universos diferentes entre numerador e denominador.

## Pesos, qualidade e limites

A referência usa 40% domicílios ocupados, 30% rendimento, 20% saturação invertida e 10% ocupação 14+. Os cenários alternativos, nessa ordem, são Pesos iguais (25/25/25/25), Ênfase mercado (50/25/15/10) e Menor saturação (30/25/35/10). São escolhas gerenciais, não estimativas de retorno.

Os limites min–max permanecem fixos no universo estadual da versão validada. Sem valor válido ou sem variação, não se atribui score arbitrário. `X`, `..` e `...` são nulos; `-` é zero absoluto publicado, com bruto preservado. Os quatro componentes precisam estar disponíveis para gerar índice, sem redistribuição silenciosa dos pesos.

Consulte os [endpoints e metadados](APIs.md), a [metodologia](../docs/metodologia.md) e o [relatório](../docs/relatorio.md). Renda nominal e ocupação não substituem pesquisa de consumo, custos, margens ou estudo de viabilidade.
