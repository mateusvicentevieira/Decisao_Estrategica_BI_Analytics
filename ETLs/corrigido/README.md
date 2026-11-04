# Coleta validada

Estado verificado em 03/11/2026: versão final `20261103_135300`, tabela `bi_validado.fontes_20261103_135300`, 2.360 registros (oito séries com 295 municípios e valores válidos em cada). `dados/20261103_135300/manifest.json` identifica essa carga. A versão anterior `135041` foi substituída por esta para corrigir o tratamento do zero publicado; pastas de tentativas anteriores não são fontes de produção.

As contagens de `public.normalizacao` (2.655), `public.caged_municipio` (294), `public.moradores_municipio` (295) e `public.domicilios_municipio` (295) coincidiram com a inspeção anterior. Não foi registrado checksum anterior; a preservação é sustentada pelo escopo dos comandos (escrita apenas em schema novo), além dessas contagens. As cargas antigas e seus scripts ficam preservados para auditoria; o pipeline atual usa este coletor e a versão final indicada.

Este coletor substitui a seleção de fontes utilizada pelos ETLs antigos, sem executar nem modificar suas tabelas. Requer `requests`, `psycopg` e `python-dotenv`, já disponíveis no ambiente do projeto.

Execute `python -m unittest test_coletor.py` nesta pasta. Execute `python coletor.py` para coletar e validar; acrescente `--carregar` para criar uma tabela nova em `bi_validado.fontes_<dataUTC>`. Cada execução cria uma versão independente. Uma falha na carga reverte a transação; `public` nunca é escrito. As credenciais são lidas do `.env` de rendimento mediano; não são copiadas para artefatos.

Cada pasta `dados/<dataUTC>` guarda respostas oficiais, metadados, snapshot longo `fontes.json` e `manifest.json` com URLs, unidades, universos, período, contagens, hash SHA-256 e tabela criada. A variável de domicílios tem unidade oficial **Domicílios**; as unidades locais CEMPRE têm unidade **Unidades**.

As seis séries de 2022 são população residente total, domicílios particulares permanentes ocupados totais, mediana nominal mensal de rendimentos de trabalho de ocupados de 14 anos ou mais com rendimento, ocupados de 14 anos ou mais, população de 14 anos ou mais e unidades locais do grupo CNAE 47.4. O denominador e o numerador da taxa de ocupação usam exatamente a mesma tabela, período, sexo, cor e grupo de idade. A saturação de concorrência usa unidades locais / população residente do mesmo ano.

O grupo 47.4 é consultado uma única vez; classes filhas não são somadas. A série histórica de concorrentes cobre 2022, 2023 e 2024 dentro da mesma série CEMPRE. Não juntar diretamente com a série encerrada em 2021. Não usar população 2022 para calcular taxas de 2023 ou 2024. O histórico antigo de domicílios não é utilizado: seu universo difere do recorte de setores selecionados coletado anteriormente para 2022.

Os sinais oficiais `X`, `..` e `...` ficam nulos. O sinal `-` representa **zero absoluto publicado**, conforme os [sinais convencionais do IBGE](https://www.ibge.gov.br/explica/producao-agropecuaria/pa); seu valor bruto é preservado. Nenhuma ausência é imputada. Valores não finitos são rejeitados. A validação exige 295 municípios sem duplicações em cada série antes da carga.

O CAGED antigo contém todos os setores e não participa do índice. `movimento_construcao` implementa filtro de seção F ou divisões CNAE 41/42/43 para uma futura coleta de microdados, com erro explícito se a classificação não existir. Não houve download dos grandes arquivos nem carga de CAGED setorial nesta etapa.

O índice é relativo a indicadores de atratividade, não uma probabilidade ou cálculo de retorno financeiro. Os dados de 2022 representam esse ano; concorrência atual, custos e viabilidade comercial precisam de análise complementar.
