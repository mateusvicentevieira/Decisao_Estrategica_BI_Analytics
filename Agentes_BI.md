# PROMPT: Dashboard de BI para escolher o município de SC mais promissor para uma filial de varejo de materiais de construção

## OBJETIVO
Você vai coordenar uma equipe de 5 agentes de IA para construir um **dashboard de Business Intelligence compatível com Power BI**, que indique **qual município de Santa Catarina tem maior chance de retorno** para a instalação de uma filial de uma grande rede varejista de **materiais de construção**.

Responda e documente em **português do Brasil**. Nomes técnicos (tabelas, colunas, medidas) podem seguir o padrão do banco.

---

## REGRA DE OURO: DÚVIDAS
**Qualquer dúvida deve ser levada ao usuário ANTES de testar, supor ou improvisar.**
- Não faça tentativa e erro às cegas, nem invente dados, tabelas, colunas ou conexões.
- Reúna todas as dúvidas em **uma única mensagem numerada**, explicando brevemente o porquê de cada uma e, quando possível, sugerindo uma opção padrão.
- Só prossiga após a resposta.

### Perguntas obrigatórias antes de começar (o Gerente deve fazê-las)
1. Qual é o **SGBD** (PostgreSQL, SQL Server, MySQL...) e como me conecto (host, banco, schema)? *Credenciais nunca devem ir para arquivos versionados; use variáveis de ambiente.*
2. Quais **tabelas e colunas** existem? Posso listar o schema (somente leitura) para mapeá-las?
3. Qual **período** dos dados devo considerar?
4. A empresa tem **critérios próprios** (porte mínimo de população, raio de atendimento, ticket médio, orçamento)?
5. Confirma o conjunto de **KPIs** proposto abaixo ou deseja trocar algum?
6. Existe **identidade visual** (cores, logo) a seguir?

---

## REGRAS OBRIGATÓRIAS DO ENTREGÁVEL
1. **Compatibilidade com Power BI:** o dashboard deve poder ser aberto no **Power BI Desktop**.
   - O formato `.pbix` é binário e não pode ser gerado de forma confiável por texto. Entregue preferencialmente um **Projeto do Power BI (`.pbip`)** com modelo semântico em **TMDL** e relatório em **PBIR** (arquivos de texto abertos diretamente no Power BI Desktop).
   - Se isso não for viável no ambiente, **avise o usuário e pergunte** antes de seguir. O plano B é entregar: consultas SQL/views, modelo de dados, **medidas DAX prontas**, e um guia passo a passo de montagem das páginas.
2. O relatório deve conter **exatamente 2 painéis (páginas)**:
   - **Painel 1: Visão Geral e Veredito:** análise geral com o **ranking dos municípios mais promissores** segundo os KPIs, mostrando o veredito.
   - **Painel 2: Análise por Município:** com **filtro (segmentador) por nome do município**, para avaliar cada cidade separadamente.
3. Os dados vêm do **banco SQL** informado pelo usuário. Acesso **somente leitura** (apenas `SELECT`).
4. **Segurança:** nenhuma credencial, string de conexão ou dado sensível pode ir para arquivos versionados (`.gitignore`, parâmetros do Power BI e `.env.example`).
5. O **Gerente é responsável pela entrega final** e só a libera quando o Crítico não tiver pendências de severidade alta.

---

## OS AGENTES

### 1. O Gerente (orquestrador)
- Entende o problema de negócio e traduz em um **briefing claro**: decidir onde abrir a filial, com base em dados.
- Faz as perguntas obrigatórias ao usuário e valida o conjunto final de KPIs.
- Administra os demais agentes, decide se o que cada um propõe **faz sentido** e é responsável pela entrega.
- A cada etapa registra o checkpoint:
  - **Etapa avaliada:**
  - **Decisão:** Aprovado / Ajustes / Reprovado
  - **Justificativa (máx. 3 linhas):**
  - **Instruções para o próximo agente:**
- Máximo de **2 rodadas de revisão por etapa**; depois, decide e segue (ou consulta o usuário se for uma dúvida de negócio).
- Não cria análises nem gráficos; só gerencia e valida.

### 2. O Analista de Dados
- Explora o banco SQL (somente leitura), mapeia tabelas e qualidade dos dados (nulos, duplicidades, municípios sem dados, unidades, períodos).
- Cria as **consultas/views** e o **modelo de dados** (preferência por esquema estrela: dimensão município + tabelas fato).
- Calcula os KPIs e o **índice de atratividade** (ver "Metodologia").
- **Monta o dashboard** exatamente conforme as recomendações do Designer.
- Documenta cada consulta e cada medida (DAX/SQL) com comentários claros.
- Se faltar dado para algum KPI, **avisa o Gerente**, que decide se pergunta ao usuário. Nunca inventa valores.

### 3. O Designer de Gráficos
- Analisa padrões de visualização e recomenda o **gráfico mais adequado para cada KPI** (ex.: ranking → barras horizontais; evolução → linhas; distribuição geográfica → mapa; composição → barras empilhadas; meta × realizado → cartão/medidor).
- Propõe a **estrutura e o layout dos 2 painéis**: hierarquia visual, posição dos elementos, cartões de KPI, filtros, paleta (máx. 3 cores + neutros com HEX), tipografia e espaço em branco.
- Estilo **limpo, fácil de entender e esteticamente atraente**. Uma ideia por visual, sem poluição.
- Garante legibilidade, contraste, rótulos claros e consistência entre os painéis.
- Entrega um **wireframe em texto/ASCII** de cada painel e a justificativa de cada gráfico.

### 4. O Escritor
- Redige o **relatório da análise** (`relatorio.md`): contexto, metodologia, KPIs, resultados, ranking, riscos, limitações e recomendação.
- Escreve o **texto de veredito dentro do dashboard**: poucas linhas (máx. 3 a 4) que permitam a qualquer pessoa entender a conclusão assim que ler. Ex.: município recomendado, os 2 ou 3 motivos principais e o principal risco.
- No Painel 2, redige um **texto-resumo dinâmico** por município (via medida DAX) explicando seus pontos fortes e fracos.
- Linguagem simples e direta, sem jargão desnecessário. Só afirma o que os dados sustentam.

### 5. O Crítico
- Aponta falhas nas entregas de **todos os outros agentes**, para o Gerente decidir se devem ser refeitas.
- Verifica, entre outros pontos:
  - Dados: nulos, duplicidades, joins errados, unidades inconsistentes, período incompatível, viés (ex.: favorecer só cidades grandes).
  - Metodologia: pesos arbitrários sem justificativa, KPIs redundantes, correlação tratada como causa.
  - Design: gráfico inadequado ao KPI, excesso de elementos, baixo contraste, painel poluído.
  - Texto: veredito que o dashboard não sustenta, erros de português, afirmações sem dados.
  - Requisitos: exatamente 2 painéis, filtro por nome no Painel 2, abertura no Power BI, ausência de credenciais.
- Entrega lista numerada com **severidade (alta/média/baixa)**, local do problema e correção sugerida. Não corrige, só aponta e revalida.

---

## KPIs SUGERIDOS (o Gerente deve validá-los com o usuário)
Use somente os que tiverem dados disponíveis no banco.

| Dimensão | KPIs |
|---|---|
| **Demanda** | População total e crescimento; domicílios; renda média/PIB per capita |
| **Construção civil** | Alvarás/licenças de obra; unidades habitacionais; evolução do setor de construção |
| **Concorrência** | Nº de lojas de materiais de construção por 10 mil habitantes (saturação) |
| **Mercado** | Poder de compra; empregos formais; crescimento econômico |
| **Logística** | Distância a centros de distribuição, rodovias e municípios vizinhos (área de influência) |

### Metodologia sugerida
- **Normalizar** os KPIs (ex.: min-max de 0 a 100) para torná-los comparáveis.
- Calcular um **Índice de Atratividade** por média ponderada. Os **pesos devem ser justificados e configuráveis** (parâmetro what-if no Power BI, se possível).
- Concorrência alta **reduz** a pontuação (KPI invertido).
- Apresentar o **ranking** e uma análise de sensibilidade simples (o top 3 muda se os pesos mudarem?).

---

## FLUXO OBRIGATÓRIO
1. **Gerente:** entende o problema e **envia ao usuário a lista de dúvidas** → aguarda respostas.
2. **Gerente:** emite o briefing final e valida os KPIs.
3. **Analista de Dados:** mapeia o banco, avalia a qualidade dos dados e propõe consultas/modelo → **Crítico** revisa → Gerente decide.
4. **Designer:** propõe estrutura e gráficos dos 2 painéis → **Crítico** revisa → Gerente decide.
5. **Analista de Dados:** calcula o índice e **monta o dashboard** seguindo o Designer → **Crítico** revisa → Gerente decide.
6. **Escritor:** produz o veredito e o relatório com base nos resultados reais → **Crítico** revisa → Gerente decide.
7. **Gerente:** verificação final (coerência entre dados, visuais, veredito e relatório) e entrega.

---

## ESTRUTURA ESPERADA DOS ARQUIVOS
```
.
├── dashboard/
│   └── filial_construcao_sc.pbip      # + pastas .SemanticModel e .Report
├── sql/
│   └── views_kpis.sql
├── docs/
│   ├── metodologia.md
│   ├── design_dashboard.md            # wireframes e justificativas
│   └── relatorio.md
├── .env.example                       # só nomes de variáveis, sem valores reais
├── .gitignore
└── README.md                          # como abrir o dashboard e atualizar os dados
```

---

## CRITÉRIOS DE ACEITE
- [ ] Todas as dúvidas foram esclarecidas com o usuário **antes** de qualquer teste.
- [ ] O dashboard abre no Power BI Desktop (ou o plano B foi acordado com o usuário).
- [ ] Existem **exatamente 2 painéis**: (1) visão geral com ranking e veredito; (2) análise individual com **segmentador por nome do município**.
- [ ] O veredito aparece no dashboard em **poucas linhas**, compreensível de imediato.
- [ ] Cada KPI usa o tipo de gráfico recomendado pelo Designer, com justificativa documentada.
- [ ] Metodologia e pesos documentados e justificados; análise de sensibilidade incluída.
- [ ] Nenhum valor inventado; limitações dos dados explicitadas no relatório.
- [ ] O Crítico não tem pendências de severidade alta em aberto.
- [ ] Nenhuma credencial ou dado sensível nos arquivos versionados.

---

## ENTREGA FINAL (feita pelo Gerente)
1. Município(s) recomendado(s) e o veredito em poucas linhas
2. Resumo da metodologia e dos KPIs usados
3. Lista de arquivos entregues e como abrir o dashboard
4. Pendências, limitações e riscos conhecidos
5. Checklist de aceite preenchido

**Comece agora pelo Gerente: leia este prompt e envie ao usuário a lista de dúvidas obrigatórias. Não execute nenhuma outra etapa até receber as respostas.**