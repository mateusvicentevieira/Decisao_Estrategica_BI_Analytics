# Design do dashboard — decisão de expansão em SC

Data: 03/11/2026. Proposta do Designer para revisão do Crítico. O desenho utiliza os requisitos e a preferência visual já delegados pelo usuário. O relatório terá **exatamente duas páginas**, sem páginas ocultas de tooltip ou drillthrough.

## Direção visual

O fundo bege, os cartões claros e os detalhes laranja retomam as referências `backgounds para os graficos.jpg` e `imagem icones.jpg`. Os gráficos ficam sobre superfícies claras, com ornamentos discretos fora da área de dados. Os arquivos de referência não serão aplicados como uma imagem única atrás dos gráficos: seus quatro blocos e ícones não correspondem às posições deste relatório.

| Uso | HEX | Regra |
|---|---|---|
| Laranja principal | `#B85016` | Barras, seleção, botões e pequenos destaques. Texto branco somente em áreas preenchidas com esta cor. |
| Laranja suave | `#F3CEAC` | Realce de seleção e detalhes decorativos; nunca texto pequeno sobre branco. |
| Bege de fundo, neutro | `#F7F2E9` | Fundo das duas páginas. |
| Superfície, neutro | `#FFFFFF` | Cartões e painéis. |
| Texto principal, neutro | `#392D25` | Títulos, valores e rótulos. |
| Texto secundário, neutro | `#685B50` | Subtítulos, unidades e notas. |
| Borda, neutro | `#E4DACD` | Divisores e contornos leves. |

São duas cores de destaque mais neutros. Nenhuma interpretação depende exclusivamente de cor: posições no ranking, sinais, nomes e rótulos numéricos permanecem visíveis. O texto principal sobre branco/bege e o branco sobre o laranja principal têm contraste adequado para leitura. Confirmar o contraste e o tamanho aparente no Power BI após a montagem.

Tipografia: **Segoe UI**, disponível no Windows. Título 26 pt, subtítulo 13 pt, títulos de visual 16 pt, rótulos e tabelas 12–14 pt, valores de cartão 28–32 pt, notas 11 pt. Números em formato pt-BR, com separadores de milhares. Índice com uma casa decimal e sufixo `/100`; taxas com uma casa decimal e `%`; renda em `R$` com rótulo do conceito. O cartão não abrevia números que precisem ser comparados com precisão; tooltips podem informar o valor completo.

Tela: **1600 × 900**, margem externa de 32 px, intervalo de 24 px entre painéis e espaço interno de 16 px. Cantos de 12 px, borda de 1 px, sem sombra forte, gradiente ou textura na área dos dados. Eixos sem grades verticais; linhas horizontais apenas se ajudarem a leitura. Ícones são opcionais e não substituem rótulos.

## Regras analíticas que o desenho precisa preservar

- O índice principal usa somente componentes de **2022** aprovados pelo Analista e pelo Crítico. A escolha de 2022 depende da disponibilidade conceitual e temporal das fontes corrigidas; se não houver cobertura suficiente, o Gerente registra o ajuste antes da montagem.
- Dados de 2021 ou de janeiro–agosto de 2026 são contexto identificado e não entram no índice de 2022. Não haverá filtro de ano que combine silenciosamente essas fontes.
- A comparação histórica só aparece quando universo, território e conceito estiverem validados. Ausência significa “Não disponível”, nunca zero. Se uma série não passar pela validação, seu painel mostra uma nota de indisponibilidade em vez de uma linha falsa.
- Índice de atratividade é pontuação relativa, não probabilidade de retorno, ROI ou projeção de receita. A limitação aparece junto ao veredito e no rodapé.
- População e domicílios só recebem rótulo de total municipal se as fontes corrigidas comprovarem esse universo. Rendimento é identificado como mediana mensal nominal dos trabalhos dos ocupados com rendimento, conforme metadados.
- Limites da normalização e universo dos municípios elegíveis permanecem fixos para cada versão de dados; selecionar um município não recalcula os limites.

## Página 1 — Visão Geral e Veredito

Pergunta atendida: **quais municípios se destacam nos indicadores disponíveis e o resultado resiste a mudanças nos pesos?**

```text
+--------------------------------------------------------------------------------+
| Decisão de expansão · Santa Catarina                     [Visão geral] [Cidade]  |
| Atratividade relativa · base 2022 · data de atualização                          |
+------------------+------------------+------------------+-----------------------+
| Município líder  | Índice /100      | Ano de referência| Cobertura elegível    |
+------------------+------------------+------------------+-----------------------+
| Veredito em 3–4 linhas: líder, motivos comprovados e principal limitação          |
+--------------------------------------------------+-----------------------------+
| Ranking dos 10 municípios                         | Cenário de pesos            |
| Barras horizontais · eixo 0–100                    | Segmentador · seleção única |
| Nomes completos e rótulos                          +-----------------------------+
|                                                  | Top 3 por cenário           |
|                                                  | Tabela de sensibilidade     |
+--------------------------------------------------+-----------------------------+
| Fonte, versão, atualização · pontuação relativa; não é previsão de retorno       |
+--------------------------------------------------------------------------------+
```

Coordenadas em pixels; `x/y` indicam o canto superior esquerdo. O título e o conteúdo interno de cada painel ocupam o mesmo contêiner. Não criar uma forma sobreposta que cubra o visual.

| Elemento | x | y | Largura | Altura | Visual nativo e conteúdo |
|---|---:|---:|---:|---:|---|
| Título | 32 | 24 | 1050 | 36 | Caixa de texto. |
| Subtítulo da base | 32 | 66 | 1050 | 22 | Texto/medida com ano e atualização. |
| Navegação: visão geral | 1236 | 24 | 156 | 40 | Botão de navegação da página atual. |
| Navegação: município | 1416 | 24 | 152 | 40 | Botão para a página 2. |
| Município líder | 32 | 112 | 368 | 96 | Cartão de texto. |
| Índice do líder | 424 | 112 | 368 | 96 | Cartão numérico, escala explícita. |
| Ano do índice | 816 | 112 | 368 | 96 | Cartão com 2022, obtido da versão aprovada. |
| Cobertura | 1208 | 112 | 360 | 96 | Cartão `elegíveis / total cadastrado`; não fixar a cobertura antes da validação. |
| Veredito | 32 | 232 | 1536 | 82 | Cartão de texto dinâmico com quebra de linha, 3–4 linhas. |
| Ranking top 10 | 32 | 338 | 920 | 482 | Barras horizontais, eixo de 0 a 100, município no eixo vertical. |
| Cenário de pesos | 976 | 338 | 592 | 110 | Segmentador de cenários aprovados, seleção única. |
| Sensibilidade top 3 | 976 | 472 | 592 | 348 | Tabela com cenário, posição, município e índice; três posições por cenário. |
| Rodapé | 32 | 844 | 1536 | 28 | Fonte resumida, atualização e limitação. |

**Ranking:** ordenar por índice decrescente; em empate usar regra documentada pelo Analista, sem sugerir superioridade estatística. Exibir índice com uma casa decimal e posição, sem ocultar empates reais. O eixo começa em zero e termina em 100 em todos os cenários. Nomes longos devem caber sem reticências que confundam municípios; reservar aproximadamente 300 px para os rótulos do eixo vertical.

**Cenários:** apresentar pelo menos o cenário de referência e duas alternativas justificadas na metodologia. Os nomes devem informar a ênfase real dos pesos. O segmentador muda o ranking, os cartões e o veredito em conjunto. A tabela de sensibilidade mantém todos os cenários visíveis para verificar estabilidade do top 3. Se o modelo usar parâmetros de peso em lugar de cenários, preservar esta área e os rótulos de peso efetivo, com validação da soma; o mecanismo será definido pelo Analista.

**Interações:** selecionar uma barra não deve transformar o município clicado em “líder” nos cartões nem reduzir a cobertura do ranking. Desativar essa interação sobre cartões, veredito, cenários e sensibilidade. A página 2 é a área de seleção individual. O título do ranking deve indicar “Top 10 · cenário [nome] · 2022”. A tabela de sensibilidade pode usar duas linhas por célula se necessário, sem reduzir a fonte abaixo de 12 pt.

**Veredito:** o Escritor fornecerá medida dinâmica com município líder, dois motivos sustentados pelos componentes e uma limitação. Não prometer retorno financeiro. Se não houver município elegível, os cartões e o veredito exibem “Sem base validada para recomendar”, sem reaproveitar um resultado anterior.

## Página 2 — Análise por Município

Pergunta atendida: **quais fatores explicam a posição deste município e qual contexto temporal está disponível?**

```text
+--------------------------------------------------------------------------------+
| Análise por município                                    [Visão geral] [Cidade]  |
| Selecione um município · componentes do índice no mesmo ano                      |
+------------------------------------+-------------------------------------------+
| Município [segmentador com busca]   | Resumo dinâmico · forças e limitações     |
+------------------+-----------------+------------------+------------------------+
| Índice /100      | Posição estadual| População total | Domicílios ocupados     |
+--------------------------------------+-----------------------------------------+
| Componentes do índice · 2022          | Evolução histórica validada             |
| Barras horizontais de contribuição   | Linha ou aviso de indisponibilidade     |
|                                      +-----------------------------------------+
|                                      | Contexto de outros períodos             |
|                                      | Tabela com valor, unidade e período     |
+--------------------------------------+-----------------------------------------+
| Fonte, versão e atualização · renda/concorrência/contextos com conceitos claros   |
+--------------------------------------------------------------------------------+
```

| Elemento | x | y | Largura | Altura | Visual nativo e conteúdo |
|---|---:|---:|---:|---:|---|
| Título | 32 | 24 | 1050 | 36 | Caixa de texto. |
| Subtítulo | 32 | 66 | 1050 | 22 | Regra de leitura e cenário ativo. |
| Navegação: visão geral | 1236 | 24 | 156 | 40 | Botão para página 1. |
| Navegação: município | 1416 | 24 | 152 | 40 | Botão da página atual. |
| Segmentador município | 32 | 112 | 520 | 88 | Nome completo, lista suspensa com busca, seleção única, sem “Selecionar tudo”. |
| Resumo do município | 576 | 112 | 992 | 88 | Cartão de texto dinâmico, até quatro linhas. |
| Índice municipal | 32 | 224 | 368 | 96 | Cartão `/100`, ano e cenário no título. |
| Posição estadual | 424 | 224 | 368 | 96 | Cartão `posição / elegíveis`, universo estadual fixo. |
| População municipal | 816 | 224 | 368 | 96 | Cartão, conceito total e ano explícitos. |
| Domicílios ocupados | 1208 | 224 | 360 | 96 | Cartão, somente se esse for o conceito validado. |
| Componentes | 32 | 344 | 744 | 476 | Barras horizontais de contribuição ao índice: score × peso efetivo. |
| Histórico comparável | 800 | 344 | 768 | 240 | Gráfico de linhas de domicílios, apenas anos comparáveis validados. |
| Contexto temporal | 800 | 608 | 768 | 212 | Tabela de indicadores contextuais com valor, unidade, período e status. |
| Rodapé | 32 | 844 | 1536 | 28 | Fontes, atualização e ressalva da pontuação. |

**Seleção:** manter um município selecionado; o nome do município deve constar no resumo. A escolha inicial será definida com os dados reais, sem gravar um nome fictício. Se nenhuma cidade ou mais de uma chegar ao contexto por filtros externos, a medida de resumo orienta “Selecione um município”; não mostrar totais de várias cidades como valor individual.

**Componentes:** exibir nomes legíveis, contribuições em pontos do índice e peso no tooltip. O total das contribuições deve corresponder ao índice. A normalização permanece estadual; o score do único município selecionado não se torna automaticamente 100. Componentes sem dado impedem a pontuação conforme a política de elegibilidade, em vez de receber zero arbitrário.

**Histórico:** eixo cronológico numérico, anos efetivos assinalados e ausência sem interpolação enganosa. Não supor que 1980, 1991, 2000, 2010 e 2022 sejam comparáveis apenas por estarem na mesma tabela. Se houver só um ano validado, usar uma tabela pequena do valor e ano dentro deste painel, com a nota “Série comparável ainda indisponível”.

**Contexto:** priorizar renda mediana nominal do trabalho e concorrência se disponíveis, com período exato; dados de emprego geral jan–ago/2026 devem ter esse rótulo quando não houver coleta setorial validada. Quando um desses dados integrar o índice de 2022, a tabela informa essa condição. Não converter salário em poder de compra real nem unidades locais em empresas únicas. Limitar a tabela aos indicadores que cabem com fonte legível, habilitando tooltip para definição completa.

**Cenário:** usar o mesmo cenário da página 1 via segmentador sincronizado, oculto nesta página (não uma página extra), e mostrar o nome no subtítulo. Nenhuma seleção de cidade altera os cenários da tabela de sensibilidade da página 1. Botões de navegação preservam o contexto do cenário.

## Escolhas de visual e justificativas

| Indicador ou tarefa | Visual | Justificativa |
|---|---|---|
| Ranking municipal | Barras horizontais | Permite comparar magnitudes e ler nomes longos sem girar texto. |
| Município líder, índice, referência e cobertura | Cartões | Resposta imediata, com unidade e universo explícitos. |
| Sensibilidade do top 3 | Tabela por cenário | Mostra nomes e posições com precisão; evita muitas séries ou linhas cruzadas. |
| Veredito e resumo local | Cartões de texto dinâmico | Conecta o resultado às evidências e limitações em linguagem direta. |
| Explicação do índice | Barras de contribuição | Expõe o efeito dos pesos e permite conferir a soma dos pontos. |
| Domicílios em anos comparáveis | Linha com marcadores | Expressa sequência temporal; os anos efetivos e a validação do universo ficam visíveis. |
| Renda, unidades locais e emprego em períodos distintos | Tabela contextual | Mantém unidade e período junto ao valor, evitando comparação temporal implícita. |
| Município individual | Segmentador por nome com busca | Atende a seleção exigida e facilita localizar qualquer município. |

Não usar mapa como visual principal: a localização não substitui ranking, e logística/área de influência ainda não têm dados aprovados. Não usar velocímetro para o índice sem uma meta empresarial definida. Não usar gráfico de pizza para pontos de indicadores com direções e unidades diferentes.

## Contrato para implementação e revisão

Os nomes desta proposta descrevem papéis semânticos, não tabelas ou medidas já existentes. O Analista deverá mapear cada papel para campos reais aprovados, documentando isso na metodologia: município, índice do cenário, posição, cobertura, componente, peso efetivo, contribuição, indicador contextual, unidade, período e fonte. Nenhum nome de coluna é presumido por este documento.

Antes da entrega, conferir no Power BI Desktop: exatamente duas páginas; abertura sem erro; segmentador por nome; nomes longos legíveis; ordem correta do ranking; índice no intervalo 0–100; coerência cartões/veredito/cenário; soma das contribuições; isolamento dos períodos; ausência exibida como indisponível; contraste; nenhum contêiner ou texto cortado. O Crítico revisará a proposta e a implementação real; esta especificação não comprova que o relatório já existe ou abre.
