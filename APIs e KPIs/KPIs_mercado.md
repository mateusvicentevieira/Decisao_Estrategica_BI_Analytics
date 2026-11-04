# KPIs — Mercado

Atualizado em 04/11/2026. Esta versão substitui a documentação dos indicadores de mercado anteriores. O índice utiliza somente dados municipais de 2022 da camada SQL corrigida; o histórico de concorrência fica separado.

## Domicílios particulares permanentes ocupados

Fonte: [IBGE, agregado 4712, variável 381, 2022](https://servicodados.ibge.gov.br/api/v3/agregados/4712/periodos/2022/variaveis/381?localidades=N6%5BN3%5B42%5D%5D), sem classificação adicional. Unidade: domicílios.

Representa o porte do mercado residencial existente. Não mede novas construções, imóveis desocupados nem todo o estoque imobiliário. Recebe score min–max direto: `100 × (valor − mínimo estadual) / (máximo estadual − mínimo estadual)`.

**Peso de referência: 40% do índice total.** Os limites são estaduais e fixos por versão; escolher um município no painel não altera o score.

## População residente total

Fonte: [IBGE, agregado 4709, variável 93, 2022](https://servicodados.ibge.gov.br/api/v3/agregados/4709/periodos/2022/variaveis/93?localidades=N6%5BN3%5B42%5D%5D), sem classificação adicional. Unidade: pessoas.

A população contextualiza o mercado e é o denominador da saturação. **Não recebe peso adicional**, para evitar pontuar duas vezes o porte já representado por domicílios. Os antigos valores de moradores do agregado 6750/9598 são recorte de entorno e não podem substituir este total.

## Saturação de unidades locais varejistas

Fonte: [CEMPRE, agregado 9528, variável 706, 2022](https://servicodados.ibge.gov.br/api/v3/agregados/9528/periodos/2022/variaveis/706?localidades=N6%5BN3%5B42%5D%5D&classificacao=12762%5B117452%5D). Classificação `12762[117452]`: grupo CNAE 47.4, comércio varejista de material de construção. Unidade original: unidades locais.

```text
Saturação = 10.000 × unidades locais CNAE 47.4 de 2022 / população residente de 2022
Score inverso = 100 × (máximo estadual − saturação) / (máximo estadual − mínimo estadual)
```

**Peso de referência: 20% do índice total.** Menor densidade de concorrentes recebe maior score por hipótese gerencial. Isso não comprova demanda reprimida: uma densidade baixa também pode refletir características de mercado ausentes do modelo.

O grupo é consultado uma vez. Não se somam grupos a suas classes filhas nem a construção civil e atacado. Unidades locais não equivalem a empresas únicas, redes, capacidade de venda ou faturamento. Os totais antigos do agregado 6450, com categorias sobrepostas, não alimentam o modelo atual.

## Composição e comparação

A referência completa é 40% domicílios + 30% rendimento do trabalho + 20% saturação invertida + 10% ocupação 14+, com todos os componentes normalizados de 0 a 100 e pertencentes a 2022. Os três cenários alternativos testam pesos iguais (25/25/25/25), ênfase em mercado (50/25/15/10) e menor saturação (30/25/35/10), nessa mesma ordem de componentes.

A série de unidades locais de 2022, 2023 e 2024 é contexto histórico comparável dentro do CEMPRE 9528; não muda o ano do índice nem usa população de outro período para formar taxas. Os [endpoints e classificações completos](APIs.md), a [metodologia](../docs/metodologia.md) e os [resultados](../docs/relatorio.md) documentam a versão usada.

Ausências permanecem nulas; o marcador oficial `-` é zero absoluto publicado. Sem os quatro componentes válidos ou sem variação para normalizar, não se cria pontuação arbitrária. O índice é relativo, com pesos gerenciais e sensibilidade a extremos; não calcula retorno financeiro.
