# KPIs — Histórico disponível e crescimento excluído

Atualizado em 04/11/2026. O índice final não contém um componente denominado “crescimento”. A documentação anterior previa indicadores cuja disponibilidade ou comparabilidade não foi confirmada. O histórico válido usado no painel é o de unidades locais varejistas, apresentado separadamente do índice de 2022.

## Histórico comparável: unidades locais CNAE 47.4

Fonte: IBGE/CEMPRE, agregado 9528, variável 706, classificação `12762[117452]`, grupo 47.4 do comércio varejista de material de construção. Endpoints: [2022](https://servicodados.ibge.gov.br/api/v3/agregados/9528/periodos/2022/variaveis/706?localidades=N6%5BN3%5B42%5D%5D&classificacao=12762%5B117452%5D), [2023](https://servicodados.ibge.gov.br/api/v3/agregados/9528/periodos/2023/variaveis/706?localidades=N6%5BN3%5B42%5D%5D&classificacao=12762%5B117452%5D) e [2024](https://servicodados.ibge.gov.br/api/v3/agregados/9528/periodos/2024/variaveis/706?localidades=N6%5BN3%5B42%5D%5D&classificacao=12762%5B117452%5D).

A série mede quantidades de unidades locais por município, sem somar grupos a classes filhas. Sua evolução não mede crescimento de obras, faturamento, capacidade concorrencial ou demanda por materiais. O gráfico usa os anos observados. A nova série iniciada em 2022 não é concatenada à série CEMPRE encerrada em 2021.

**Peso do histórico no índice: zero.** Somente as unidades locais de 2022 entram no cálculo da saturação de 2022: `10.000 × unidades locais / população residente do mesmo ano`. Não se usa a população de 2022 como denominador para 2023 ou 2024.

## Indicadores excluídos e motivos

| Indicador anterior | Estado no modelo atual | Motivo |
|---|---|---|
| Moradores 2022, agregado 6750/9598 | Substituído por população residente total 4709/93. | Recorte de setores da Pesquisa Urbanística do Entorno não representa total municipal. |
| Domicílios 2022 do agregado 10053/9599 e crescimento histórico anterior | Fora do índice e do gráfico histórico. | O recorte de entorno de 2022 é incompatível com o universo das séries antigas; diferenças não comprovam crescimento ou queda de domicílios. |
| Razão de dependência | Sem peso no índice. | Corte anterior de 0–14 e 70+ contra 15–69 é próprio e seu papel na atratividade de expansão não foi validado. |
| Proporção em idade ativa | Fora do índice. | A população de 15–69 anos e os moradores do recorte de entorno não formam proporção municipal válida. |
| CAGED disponível, janeiro–agosto/2026 | Fora do índice. | Coleta geral de SC, sem recorte setorial comprovado; oito meses não são 12 meses. Não mede novas construções. |
| Soma antiga de empresas CEMPRE 6450 | Substituída pelo grupo exclusivo 47.4 do agregado 9528. | Misturava construção, atacado e varejo e somava categorias hierárquicas sobrepostas. |

O CAGED setorial não foi recoletado nesta versão. O coletor contém uma função para selecionar seção F ou divisões CNAE 41/42/43 em eventual microdado futuro, mas a existência da função não significa que dados setoriais tenham sido baixados, carregados ou usados. Mesmo um saldo setorial válido seria proxy de emprego, não quantidade de obras.

Não calcular a fórmula histórica `(valor atual − valor anterior) / valor anterior × 100` sobre os domicílios legados até comprovar universos, território e conceitos compatíveis. Os dados antigos e a normalização exploratória são preservados para auditoria e não devem ser reutilizados como fontes do modelo corrigido.

## Composição efetivamente utilizada

O índice é uma média ponderada dos scores de 2022: domicílios particulares permanentes ocupados (40%), rendimento nominal mediano mensal do trabalho (30%), saturação de unidades locais por 10 mil habitantes em direção inversa (20%) e taxa de ocupação de pessoas de 14 anos ou mais (10%). Os limites min–max estaduais são fixos por versão.

Três cenários alternativos usam, nessa ordem de componentes, Pesos iguais (25/25/25/25), Ênfase mercado (50/25/15/10) e Menor saturação (30/25/35/10). Os cenários avaliam sensibilidade aos pesos; não alteram períodos nem adicionam o histórico ao índice. Os pesos são hipóteses gerenciais, sem validação causal de retorno.

Ausência permanece nula, sem interpolação ou conversão automática em zero. O marcador oficial `-` é zero absoluto publicado; `X`, `..` e `...` são nulos. Consulte as [fontes oficiais completas](APIs.md), a [metodologia](../docs/metodologia.md) e os [resultados e limitações](../docs/relatorio.md). Obras novas, alvarás, logística e viabilidade financeira permanecem fora da base.
