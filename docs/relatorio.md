# Relatório de análise — filial de materiais de construção em SC

Data: 03/11/2026. Resultados da versão SQL `bi_validado.fontes_20261103_135300`, exportada em 03/11/2026 às 10:55:39, horário de Brasília. A verificação do projeto Power BI e a liberação final são registradas nos [checkpoints](briefing_e_checkpoints.md); o ranking analítico não substitui essas verificações.

## Contexto

O objetivo é priorizar municípios catarinenses para estudo comercial de instalação de uma filial varejista de materiais de construção. Não foram informados filtros comerciais mínimos. A equipe utiliza indicadores públicos municipais e preserva os dados originais, conforme autorização de correção e nova coleta.

## Método

O índice de atratividade combina apenas dados de 2022: domicílios particulares permanentes ocupados (40%), rendimento nominal mediano mensal do trabalho (30%), saturação de unidades locais do varejo CNAE 47.4 por 10 mil habitantes, invertida (20%), e taxa de ocupação de pessoas de 14 anos ou mais (10%). Os scores min–max têm limites estaduais fixos por versão. Os pesos são hipóteses gerenciais; o índice não é probabilidade de retorno ou ROI. As definições, fontes, regras de ausência e três cenários alternativos constam na [metodologia](metodologia.md).

## Resultados e sensibilidade

As oito séries coletadas contêm 2.360 registros, correspondentes a 295 municípios por série. Todos os 295 municípios possuem os quatro componentes válidos para o índice de 2022. Os dados abaixo foram extraídos de `dashboard/resultados.json`, produzido a partir do snapshot SQL, e apresentados com uma casa decimal.

**Florianópolis é a primeira prioridade para estudo comercial segundo este índice**, com 90,1/100 no cenário de referência, seguida de Joinville (77,5) e Blumenau (67,4). O município combina 219.739 domicílios particulares permanentes ocupados com rendimento mediano mensal do trabalho de R$ 3.000 em 2022. O resultado indica destaque nos indicadores escolhidos; não demonstra maior retorno financeiro esperado.

| Posição na referência | Município | Índice /100 |
|---|---|---:|
| 1 | Florianópolis | 90,1 |
| 2 | Joinville | 77,5 |
| 3 | Blumenau | 67,4 |
| 4 | São José | 59,3 |
| 5 | Chapecó | 58,3 |
| 6 | Balneário Camboriú | 57,2 |
| 7 | Itajaí | 56,6 |
| 8 | Jaraguá do Sul | 54,7 |
| 9 | Palhoça | 52,6 |
| 10 | Criciúma | 52,1 |

Na referência, Florianópolis recebe aproximadamente 39,6 pontos pelo mercado residencial, 30,0 pelo rendimento, 13,7 pela menor saturação e 6,8 pela ocupação. A soma usa precisão completa e resulta em 90,14865; parcelas arredondadas podem diferir do total exibido. O score residencial é 98,995/100, próximo do máximo estadual, e o rendimento atinge o máximo observado, compartilhado com outros municípios. Isso não significa exclusividade de liderança em renda.

A taxa de ocupação de Florianópolis é 63,3%: 290.783 ocupados entre 459.243 residentes de 14 anos ou mais. Sua saturação é 13,0 unidades locais CNAE 47.4 por 10 mil habitantes: 697 unidades locais para 537.211 habitantes. Os scores desses componentes são 68,4 e 68,5, respectivamente; portanto, sua liderança global não decorre de liderar todos os indicadores.

| Cenário | 1º — Florianópolis | 2º — Joinville | 3º — Blumenau |
|---|---:|---:|---:|
| Referência | 90,1 | 77,5 | 67,4 |
| Pesos iguais | 84,0 | 72,8 | 69,5 |
| Ênfase mercado | 91,6 | 81,3 | 66,7 |
| Menor saturação | 85,5 | 73,7 | 67,7 |

Os três primeiros municípios mantêm a mesma ordem nos quatro cenários. Essa estabilidade limita a dependência do top 3 às quatro configurações testadas; não valida causalmente os pesos nem assegura estabilidade sob outros indicadores, períodos ou hipóteses comerciais.

## Comparação entre anos

O histórico comparável disponível é a quantidade de unidades locais CNAE 47.4 na mesma série CEMPRE. No conjunto de SC, são 12.844 em 2022, 13.510 em 2023 e 13.847 em 2024. Em Florianópolis, são 697, 727 e 747, respectivamente. O aumento indica mais unidades locais registradas nesse grupo, sem medir capacidade de venda, faturamento ou entrada de redes específicas. O histórico não integra o índice de 2022 e não é transformado em saturação de 2023/2024 usando a população de 2022.

O histórico antigo de domicílios foi excluído por universos incompatíveis, e o CAGED geral de janeiro a agosto de 2026 não representa emprego da construção civil.

## Riscos e limites

Os dados do índice retratam 2022. O modelo não contém orçamento, margem, custos de implantação e operação, área de influência, imóveis, alvarás, capacidade de concorrentes ou receitas projetadas. Domicílios ocupados medem porte residencial; unidades locais são proxy de concorrência; rendimento do trabalho não é renda domiciliar per capita. Resultados devem priorizar investigação comercial, sem prometer retorno.

## Verificação e aceite

Entrega aprovada em 04/11/2026. O projeto foi aberto e atualizado no Power BI Desktop; as duas páginas, ranking, filtro por nome, cenários sincronizados, contribuições e textos foram conferidos. O Crítico encerrou as pendências altas. O [checklist preenchido](checklist_aceite.md), a [revisão final](revisao_final.md) e os [checkpoints](briefing_e_checkpoints.md) registram o aceite e a distinção entre evidência nativa e inspeção estática.

Os oito testes do coletor e os treze testes de cálculos, estrutura e verificador foram aprovados. A validação final conferiu 34 documentos com zero falhas: 21 contra o esquema declarado, dez por compatibilidade integral com esquema público apenas em memória e três descritores pelo esquema público identificado pela extensão. O Desktop usou uma versão de esquema ainda não publicada para esses dez visuais; não se alega validação contra o esquema indisponível. Quatro JSON auxiliares sem esquema não integram a contagem. Os detalhes constam em [validacao_estrutura.json](validacao_estrutura.json).
