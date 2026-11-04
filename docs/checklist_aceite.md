# Checklist de aceite — 04/11/2026

**Decisão do Gerente: entrega aprovada.** Revisão crítica final: `revisao_final.md`, sem pendências de severidade alta em aberto. Os checkpoints registram a distinção entre inspeção estática, testes e conferência efetiva no Power BI Desktop.

- [x] Perguntas obrigatórias respondidas; ampliação para corrigir ETLs e recoletar fontes autorizada expressamente, preservando dados existentes.
- [x] Projeto `dashboard/filial_construcao_sc.pbip` aberto no Power BI Desktop instalado. Modelo carregado e atualização dos dados incorporados executada.
- [x] Exatamente duas páginas: Visão Geral e Veredito; Análise por Município.
- [x] Ranking top 10 e veredito curto na visão geral, com ano e cobertura identificados.
- [x] Segmentador por nome na segunda página, com busca e seleção municipal verificados; cenário sincronizado entre páginas.
- [x] Aparência bege e laranja, wireframes e justificativas dos visuais em `design_dashboard.md`.
- [x] Índice usa somente componentes de 2022; pesos de referência 40/30/20/10 e três alternativas documentados.
- [x] Sensibilidade incluída. Florianópolis, Joinville e Blumenau mantêm a mesma ordem nos quatro cenários testados.
- [x] Limites estaduais de normalização fixos, concorrência invertida e componentes municipais conferidos.
- [x] Fontes oficiais corrigidas em `bi_validado.fontes_20261103_135300`: oito séries de 295 municípios, 2.360 registros.
- [x] Zero publicado distinto de ausência; faixas etárias alinhadas e concorrência sem sobreposição de categorias.
- [x] Histórico de unidades locais 2022–2024 separado do índice; séries incompatíveis e CAGED geral excluídos da pontuação.
- [x] Dados originais de `public` e backup preservados. Nenhum valor foi inventado; limitações no relatório.
- [x] Credenciais não incorporadas ao projeto. `.env.example` contém apenas chaves vazias; `.gitignore` cobre ambientes e caches locais.
- [x] Treze testes do relatório/verificador e oito do coletor aprovados. Validação de 34 documentos com zero falhas: 21 pelo esquema declarado, dez por compatibilidade pública integral em memória e três por esquema público identificado pela extensão; quatro JSON auxiliares sem esquema excluídos explicitamente. Evidência em `validacao_estrutura.json`.
- [x] Crítico sem pendências altas em aberto; revisão final e decisão de liberação documentadas.

## Evidência de interação

No cenário Referência, o Desktop mostrou Florianópolis com 90,1/100 e cobertura de 295 municípios. Pesos iguais alterou o resultado para 84,0 nas duas páginas. A seleção de Florianópolis mostrou contribuições correspondentes e histórico de 697, 727 e 747 unidades locais. O texto dinâmico informa ponto forte e menor score relativo.

O ajuste final de unidade foi demonstrado na interface para população (537.211) e aplicado pela mesma propriedade nativa ao cartão de domicílios (219.739). O projeto fica com Referência e Florianópolis como seleções iniciais e Visão Geral como página de abertura.

## Limites e atualização

A pontuação prioriza estudo comercial com indicadores de 2022. Não mede ROI, lucro nem probabilidade de sucesso. O modelo não contém custos, margens, logística ou demanda efetiva. A estabilidade observada vale para os quatro cenários apresentados.

O projeto incorpora agregados públicos exportados do PostgreSQL. O botão Atualizar do Desktop relê o snapshot incorporado; uma coleta/exportação nova segue os comandos do README. As pastas `.Report` e `.SemanticModel` precisam acompanhar o `.pbip`.
