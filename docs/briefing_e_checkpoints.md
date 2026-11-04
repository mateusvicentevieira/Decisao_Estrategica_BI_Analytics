# Briefing e checkpoints do Gerente

Data: 03/11/2026. Guia: `../Agentes_BI.md`.

## Objetivo autorizado

Apoiar a seleção de município de Santa Catarina para filial de varejo de materiais de construção, com dados reais do PostgreSQL. Entrega prevista: projeto Power BI com exatamente duas páginas — Visão Geral e Veredito; Análise por Município com segmentador por nome —, consultas, metodologia e relatório em português.

O usuário delegou a seleção dos KPIs e a aparência. Preferência visual: bege e laranja, fundo minimalista inspirado nas imagens locais. Os dados são tratados como brutos e precisam de validação. Não há critérios comerciais adicionais informados.

Todos os anos disponíveis podem ser analisados. Fórmulas de composição, razões e índices precisam de componentes do mesmo período. Comparações históricas devem preservar conceitos, território e janelas equivalentes; mudanças entre anos não autorizam misturar anos de indicadores distintos numa mesma pontuação.

Permissões iniciais: consultar todas as tabelas e editar somente `normalizacao`. Posteriormente o usuário autorizou corrigir ETLs e recoletar fontes, preservando os dados atuais. A nova camada utiliza schema separado `bi_validado`; não houve escrita nas tabelas originais de `public`. Credenciais dos arquivos locais de ambiente não são copiadas para documentação ou arquivos versionados.

## Checkpoint 1 — briefing

- Etapa avaliada: requisitos e autorizações.
- Decisão: Aprovado.
- Justificativa: objetivo, duas páginas, preferência visual e regra de períodos foram informados; decisões técnicas sobre KPIs foram delegadas.
- Instruções para o próximo agente: mapear banco e verificar conceitos, cobertura, ausências e comparabilidade antes de calcular ranking.

## Checkpoint 2 — fontes e qualidade

- Etapa avaliada: mapeamento do Analista e revisão do Crítico.
- Decisão: Ajustes.
- Justificativa: fontes de moradores/domicílios não representam totais municipais; empresas têm sobreposição; ocupação tem faixas incompatíveis; CAGED não está restrito à construção.
- Instruções para o próximo agente: aguardar autorização de ampliação de edição aos ETLs e fontes, ou definição de entrega descritiva provisória. Não liberar ranking de expansão com as fontes atuais.

Revisão: uma rodada concluída. Seis pendências de severidade alta e uma média registradas pelo Crítico. Detalhes e fontes oficiais em `diagnostico_inicial.md`. Não houve revisão adicional desnecessária nem aprovação da entrega final.

## Encaminhamento

Foi solicitada ao usuário autorização específica para corrigir ETLs e recoletar fontes oficiais, preservando os dados atuais. A autorização de editar `normalizacao` não abrange essas alterações nas origens. A alternativa apresentada é análise descritiva provisória sem eleição de município.

Atualização: o usuário autorizou expressamente **correções e nova coleta, preservando os dados atuais**. A equipe iniciou os ajustes em camada separada, sem sobrescrever as tabelas públicas existentes. Plano: `superpowers/plans/2026-11-03-bi-sc.md`.

O backup real foi identificado e inspecionado sem restauração. O banco atual contém uma tabela adicional de ocupados. O projeto foi construído e aberto no Power BI Desktop instalado; as verificações nativas estão registradas abaixo.

## Checkpoint 3 — desenho dos painéis

- Etapa avaliada: `design_dashboard.md`, revisão do Crítico em primeira rodada.
- Decisão: Aprovado para montagem.
- Justificativa: exatamente duas páginas, filtros e contexto temporal explícitos, ranking e sensibilidade legíveis, paleta coerente com as referências.
- Instruções para o próximo agente: montar visuais nativos e conferir abertura, medidas, seleção e aparência no Power BI; aprovação de design não equivale a validação do arquivo.

## Checkpoint 4 — primeira carga corrigida

- Etapa avaliada: coleta em camada separada e política de marcadores IBGE.
- Decisão: Ajustes.
- Justificativa: fontes contemporâneas e universos aprovados; o marcador oficial `-` representa zero absoluto e não deve excluir Flor do Sertão do índice.
- Instruções para o próximo agente: corrigir conversão, preservar bruto e carregar nova versão; `X`, `..` e `...` continuam sem valor. Revalidar cobertura antes do índice.

## Checkpoint 5 — fontes corrigidas, segunda rodada

- Etapa avaliada: coletor, testes, README, manifesto e snapshot final `20261103_135300`.
- Decisão: Aprovado.
- Justificativa: oito séries completas com 295 municípios; zero publicado preservado; universos etários, totais e categorias de concorrência alinhados. Crítico sem pendência alta nas fontes.
- Instruções para o próximo agente: utilizar exclusivamente `bi_validado.fontes_20261103_135300` no índice e identificar o ano comum 2022; validar modelo, sensibilidade e abertura.

Fonte final: 2.360 registros. Tabelas em `public` não receberam escrita; contagens conferidas pelo Analista. CAGED setorial não foi recoletado e não entra no índice; o histórico antigo de domicílios continua excluído por incompatibilidade de universo. A série comparável de unidades locais 2022–2024 compõe o contexto histórico.

## Checkpoint 6 — modelo, cálculos e escrita

- Etapa avaliada: modelo TMDL, resultados exportados, sensibilidade, metodologia e relatório.
- Decisão: Aprovado na revisão estática, com validação nativa obrigatória.
- Justificativa: índice de 2022 e quatro cenários coerentes; fontes completas e originais preservadas. Top 3: Florianópolis, Joinville e Blumenau em todos os cenários.
- Instruções para o próximo agente: comprovar execução das medidas e leitura dos visuais no Desktop, corrigindo defeitos que schemas e inspeção não detectam.

## Checkpoint 7 — conferência nativa

- Etapa avaliada: abertura no Power BI Desktop, importação das tabelas incorporadas e seleção interativa.
- Decisão: Ajustes de formatação em encerramento.
- Justificativa: abertura e atualização executadas; ranking corrigido e visível; cenário Referência mostra 90,1/100 e 295 elegíveis. Pesos iguais mostra 84,0 nas duas páginas; seleção de Florianópolis mostra histórico 697/727/747 unidades locais.
- Instruções para o próximo agente: aplicar os números tipados identificados em JSON salvo pelo Desktop, conferir textos completos e suprimir contexto municipal sem seleção única, então salvar e revalidar.

Evidência técnica: Desktop identificou variável DAX `id` como inválida; substituída por `municipioSelecionado`. Fontes de cartões gravadas como Literal `12` eram ignoradas pelo aplicativo; a amostra ajustada na interface e salva demonstrou o formato `12D`. O veredito dessa amostra passou a aparecer completo. Essas falhas não foram detectadas pela validação de schemas, por isso o aceite depende também da conferência nativa.

## Checkpoint 8 — encerramento em 04/11/2026

- Etapa avaliada: reabertura nativa, correções pontuais, revisão final e documentação.
- Decisão: Aprovado para entrega.
- Justificativa: ranking e textos completos comprovados no Desktop; filtro municipal e cenários sincronizados funcionam. O Crítico encerrou todas as pendências altas em `revisao_final.md`.
- Instruções para uso: abrir o PBIP com as pastas associadas, usar os cenários e a seleção municipal; para dados novos, seguir o processo de atualização do README.

A reabertura final mostrou eixo de ranking 0–100, 295 elegíveis e Florianópolis com 90,1 pontos. O veredito e o resumo forte/fraco ficaram completos. População foi conferida na interface como 537.211 após selecionar unidade integral; o Desktop gravou `labelDisplayUnits = 1D`. A mesma propriedade foi aplicada a domicílios e ao gerador. O contexto usa medida protegida por seleção única; a visão geral é a página inicial e os filtros iniciais são Referência e Florianópolis.

Os nove testes de cálculos, referências e estrutura do relatório passaram na conferência de 04/11; os oito testes do coletor passaram na etapa de fontes, sem alterações posteriores nesse código. O Desktop salvou alguns arquivos com versões de esquema ainda não disponíveis nos endereços públicos da Microsoft. A validação estrutural final e as eventuais versões de compatibilidade utilizadas em memória são documentadas em `validacao_estrutura.json`; não se alega validação contra um esquema indisponível. A execução nativa constitui evidência separada.

## Estado final

Concluídos: fontes corrigidas, carga separada, revisões de fontes/design/modelo/escrita, índice e sensibilidade, duas páginas nativas, documentação, abertura e testes de seleção/cenário, correções de legibilidade e revisão final sem pendências altas.

Checklist de aceite: `checklist_aceite.md`. Limitações substantivas permanecem no relatório e não representam tarefas de implementação abertas: dados de 2022, pesos gerenciais e ausência de custos, margens e logística. Não se estima retorno financeiro.
