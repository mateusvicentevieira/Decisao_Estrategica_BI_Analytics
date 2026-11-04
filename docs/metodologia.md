# Metodologia — atratividade municipal em SC

Data: 03/11/2026. Objetivo: apoiar a priorização de municípios de Santa Catarina para estudo de implantação de filial de materiais de construção. O índice é uma comparação relativa de indicadores observados, não probabilidade de sucesso, ROI, previsão de receita ou estimativa de lucro.

## Fontes, conceitos e período

A nova coleta oficial é carregada em tabelas versionadas e longas de `bi_validado`. Cada registro identifica município, KPI, período, valor interpretado, valor bruto, unidade, universo, fonte, agregado, variável, classificação e instante de coleta. A chave é município × KPI × período. As tabelas antigas são preservadas; elas não alimentam o índice corrigido.

| Série | Fonte oficial | Conceito e uso |
|---|---|---|
| População, 2022 | [IBGE 4709](https://servicodados.ibge.gov.br/api/v3/agregados/4709/metadados), variável 93 | População residente total; denominador da saturação. Não recebe peso adicional para evitar duplicar a pontuação de porte residencial. |
| Domicílios, 2022 | [IBGE 4712](https://servicodados.ibge.gov.br/api/v3/agregados/4712/metadados), variável 381 | Domicílios particulares permanentes ocupados. Representa porte do mercado residencial existente; não mede obras novas nem todo o estoque imobiliário. |
| Rendimento, 2022 | [IBGE 10289](https://servicodados.ibge.gov.br/api/v3/agregados/10289/metadados), variável 13537 | Rendimento nominal mediano mensal de todos os trabalhos das pessoas ocupadas de 14 anos ou mais com rendimento de trabalho. Reais de 2022; não renda domiciliar per capita ou poder de compra atual. |
| Ocupados e população de 14 anos ou mais, 2022 | [IBGE 10268](https://servicodados.ibge.gov.br/api/v3/agregados/10268/metadados), variáveis 696 e 140, categoria etária 82072 | Numerador e denominador têm o mesmo grupo de idade, sexo, cor, período e universo. A categoria etária restringe a 14 anos ou mais, embora o nome geral das variáveis mencione 10 anos ou mais. |
| Unidades locais de varejo de material de construção, 2022–2024 | [IBGE/CEMPRE 9528](https://servicodados.ibge.gov.br/api/v3/agregados/9528/metadados), variável 706, grupo CNAE 47.4, categoria 117452 | Proxy de concorrência. O grupo é consultado uma única vez, sem somar classes filhas. Unidades locais não equivalem a empresas únicas, redes, capacidade de venda ou faturamento. |

O índice combina somente componentes de **2022**, ano comum das fontes aprovadas. A série de concorrentes de 2022 a 2024 permite observar quantidades, separadamente do índice. Não se divide a quantidade de 2023 ou 2024 pela população de 2022. A nova série CEMPRE não é concatenada à série encerrada em 2021.

O histórico antigo de domicílios fica bloqueado por incompatibilidade de universo. O CAGED antigo corresponde a emprego formal geral de janeiro a agosto de 2026, sem filtro setorial comprovado, e não participa do índice. Não há medida de obras novas, alvarás, logística, custos de implantação ou margens comerciais neste modelo.

## Qualidade e rastreabilidade

O coletor exige 295 municípios sem duplicação em cada série e rejeita valores não finitos. Cada execução preserva respostas oficiais, metadados, manifesto com URLs e hashes SHA-256 e o snapshot longo, permitindo identificar a versão exportada do PostgreSQL.

O marcador SIDRA `-` representa zero absoluto publicado e é convertido em zero com preservação do bruto. Os marcadores `X`, `..` e `...` são nulos; não há imputação. Zero publicado e ausência são situações diferentes. Denominadores devem ser positivos. Sem os quatro componentes válidos, o município não recebe índice; os pesos não são redistribuídos silenciosamente.

A camada de normalização anterior permanece como registro exploratório histórico. Os limites e scores do modelo corrigido são derivados da versão validada exportada do SQL; não se deve reaproveitar os scores antigos com universos incorretos.

## Cálculos

Para cada município, sempre em 2022:

```text
Taxa de ocupação 14+ (%) = 100 × ocupados 14+ / população 14+
Saturação (unidades locais por 10 mil habitantes) = 10.000 × unidades locais CNAE 47.4 / população residente
Score direto = 100 × (valor − mínimo estadual) / (máximo estadual − mínimo estadual)
Score inverso de saturação = 100 × (máximo estadual − valor) / (máximo estadual − mínimo estadual)
Índice = Σ (peso do componente × score do componente)
Contribuição em pontos = peso do componente × score do componente
```

Os pesos são frações cuja soma é 1. Domicílios, rendimento e taxa de ocupação têm direção direta; saturação tem direção inversa. Menor densidade de concorrentes é tratada como mais favorável por hipótese gerencial, embora possa também refletir menor atratividade não observada.

Os limites min–max são calculados sobre o universo estadual validado da versão e ficam fixos no relatório. Selecionar um município não os recalcula. Um componente sem variação não admite min–max e deve bloquear a composição até tratamento explícito; não atribuir 100 ou zero arbitrariamente. Valores extremos podem comprimir os scores intermediários; o índice não demonstra distância econômica proporcional entre municípios.

## Pesos e sensibilidade

| Cenário | Domicílios | Rendimento | Saturação invertida | Ocupação 14+ |
|---|---:|---:|---:|---:|
| Referência | 40% | 30% | 20% | 10% |
| Pesos iguais | 25% | 25% | 25% | 25% |
| Ênfase mercado | 50% | 25% | 15% | 10% |
| Menor saturação | 30% | 25% | 35% | 10% |

Os pesos são escolhas gerenciais propostas pela equipe, dentro da delegação do usuário, sem validação causal ou calibração por retorno de filiais. A referência dá prioridade ao mercado residencial, seguido de rendimento, pressão concorrencial e participação no trabalho. Ocupação recebe peso menor por complementar o rendimento e evitar concentrar a pontuação em mercado de trabalho. Os cenários permitem verificar se a liderança e o top 3 dependem dessas escolhas.

O relatório exibe os três primeiros de cada cenário. A comparação deve informar se os nomes e posições mudam; liderança estável entre esses quatro cenários não comprova robustez a todas as escolhas possíveis. A ordenação usa os valores completos, antes do arredondamento de exibição; resultados visualmente iguais podem conter diferenças menores que uma casa decimal. A posição estadual DAX utiliza ranking denso, preservando a mesma posição em empates exatos. Na exportação e nas seleções do líder, top 10 e três linhas de sensibilidade, o código IBGE crescente desempata apenas a ordem de apresentação, sem sugerir superioridade estatística. Um empate exato pelo índice não comprova vantagem comercial do município apresentado primeiro.

## Modelo e atualização

O Power BI recebe um snapshot público exportado exclusivamente das tabelas SQL corrigidas de `bi_validado`, incorporado por Power Query `#table`. Isso permite abrir a versão entregue sem credenciais do PostgreSQL. Um script de atualização refaz a exportação SQL e a geração do modelo; o relatório não deve ser descrito como conexão ativa com atualização automática.

O projeto deve ter exatamente duas páginas: visão geral com ranking, veredito e sensibilidade; análise por município com segmentador por nome, componentes e contexto histórico. A identificação da versão, cobertura e data de coleta deve acompanhar o relatório. Resultados reais e estado da verificação de abertura ficam em [relatório](relatorio.md) e [checkpoints](briefing_e_checkpoints.md).

## Limites para a decisão

A recomendação é uma prioridade para estudo comercial presencial, apoiada em dados de 2022, e não autorização automática de investimento. A base não contém custos, margem, orçamento, ticket médio, localização de imóveis, raio de influência, capacidade de concorrentes, fretes, alvarás ou procura efetiva por materiais. O estoque de domicílios ocupados favorece mercados maiores e não mede crescimento da construção. A mediana de rendimento do trabalho não representa toda a renda disponível dos consumidores. Antes de investir, atualizar concorrência local, estimar receitas e despesas e avaliar imóveis, logística e demanda na área de influência.
