# Decisão Estratégica — BI de expansão em Santa Catarina

Projeto Power BI com duas páginas para comparar os 295 municípios catarinenses por indicadores de atratividade para varejo de materiais de construção. Aparência em bege e laranja, conforme as referências fornecidas.

O catálogo atualizado de [APIs e fontes](APIs%20e%20KPIs/APIs.md) e os documentos de [Mercado](APIs%20e%20KPIs/KPIs_mercado.md), [Poder de Compra](APIs%20e%20KPIs/KPIs_PoderDeCompra.md) e [Crescimento](APIs%20e%20KPIs/KPIs_Crescimento.md) descrevem as fontes realmente utilizadas, os indicadores excluídos e as comparações entre anos permitidas.

**Entrega aprovada em 04/11/2026:** projeto aberto e conferido no Power BI Desktop, com duas páginas e revisão crítica sem pendências altas. [Checklist de aceite](docs/checklist_aceite.md) e [checkpoints](docs/briefing_e_checkpoints.md) registram as verificações.

**Resultado analítico:** Florianópolis lidera o cenário de referência com 90,1/100, seguida de Joinville (77,5) e Blumenau (67,4). O top 3 mantém a ordem nos quatro cenários de pesos. A prioridade é para estudo comercial; o índice não calcula ROI nem probabilidade de retorno.

## Abrir e usar

1. No Power BI Desktop, abra [dashboard/filial_construcao_sc.pbip](dashboard/filial_construcao_sc.pbip). Mantenha ao lado as pastas `.Report` e `.SemanticModel`; elas fazem parte do projeto. Se o Desktop solicitar habilitação do formato de projeto, siga a opção correspondente nas configurações da versão instalada e reabra o arquivo.
2. Em **Visão Geral e Veredito**, consulte o ranking e selecione o cenário de pesos. O índice usa somente 2022; a sensibilidade compara os três primeiros de cada cenário. Se as tabelas incorporadas ainda não estiverem carregadas na primeira abertura, clique em **Atualizar**.
3. Em **Análise por Município**, selecione um município pelo nome para ver seus componentes e o histórico de unidades locais do varejo CNAE 47.4 de 2022 a 2024.

O modelo entregue incorpora um snapshot de agregados públicos exportado do PostgreSQL. Abrir essa versão não exige credenciais do banco. O relatório não possui conexão ativa nem atualização automática: **Atualizar** no Desktop relê as tabelas incorporadas e não busca dados novos no PostgreSQL. Para incorporar nova exportação, execute o procedimento abaixo e reabra o projeto.

## Dados e método

O índice de referência usa domicílios particulares permanentes ocupados (40%), rendimento nominal mediano mensal do trabalho (30%), unidades locais varejistas CNAE 47.4 por 10 mil habitantes em direção inversa (20%) e taxa de ocupação de pessoas de 14 anos ou mais (10%). Todos os componentes são de 2022 e os limites min–max estaduais permanecem fixos ao selecionar cidades. A população serve de denominador, sem acrescentar um segundo peso de porte.

As fontes corrigidas foram carregadas em `bi_validado.fontes_20261103_135300`: oito séries de 295 municípios, total de 2.360 registros. O histórico de concorrentes 2023/2024 fica separado do índice. Os dados originais de `public` e os ETLs antigos foram preservados. `normalizacao` é a camada exploratória anterior, com fontes incompatíveis, e seus scores não alimentam o modelo corrigido.

O CAGED geral de janeiro a agosto de 2026 não entra no índice. O histórico antigo de domicílios não é comparado com o recorte de entorno de 2022. O marcador oficial `-` significa zero absoluto publicado; `X`, `..` e `...` são valores indisponíveis, sem imputação.

Consulte a [metodologia](docs/metodologia.md), o [relatório com ranking e riscos](docs/relatorio.md), o [diagnóstico histórico](docs/diagnostico_inicial.md) e o [desenho dos painéis](docs/design_dashboard.md).

## Atualizar a versão incorporada

Feche o projeto no Desktop antes de regenerar seus arquivos. Os comandos a seguir são executados na pasta deste README, com Python e as dependências `requests`, `psycopg` e `python-dotenv` disponíveis. No computador utilizado, o executável é `C:\Python314\python.exe`; ajuste apenas se sua instalação for diferente.

Para exportar novamente a versão SQL validada e reconstruir os arquivos do projeto:

```powershell
& 'C:\Python314\python.exe' scripts/build_dashboard.py --source bi_validado.fontes_20261103_135300
```

A exportação consulta o banco em modo somente leitura. As credenciais permanecem no `.env` local de rendimento mediano, na pasta de ETLs do projeto ou na pasta de ETLs vizinha; não são gravadas no PBIP. A consulta exata fica registrada em `sql/views_kpis.sql`.

Para fazer uma nova coleta oficial, com os períodos definidos no coletor, e gravar uma nova versão independente:

```powershell
& 'C:\Python314\python.exe' ETLs/corrigido/coletor.py --carregar
```

Use então o nome da tabela realmente criada, informado pelo coletor e pelo `manifest.json`, no argumento `--source` do gerador. Cada coleta preserva bruto, metadados e hashes em `ETLs/corrigido/dados/<versao>/`. Ela não transforma automaticamente o índice em um ano mais recente: mudar o período exige fontes contemporâneas compatíveis para todos os componentes e revisão da metodologia.

Para reconstruir exclusivamente a partir do snapshot já exportado, sem consultar o banco:

```powershell
& 'C:\Python314\python.exe' scripts/build_dashboard.py
```

Após a regeneração, reabra o PBIP no Desktop e confira as duas páginas, seleção de município, cenário, cobertura, totais e textos. Preserve versões anteriores quando precisar manter resultados já publicados. Não execute os ETLs antigos para atualizar a camada corrigida.

As verificações de integridade e de schemas podem ser repetidas com:

```powershell
& 'C:\Python314\python.exe' -m unittest discover -s scripts -p 'test_*.py' -v
& 'C:\Python314\python.exe' scripts/validate_pbip.py
```

A validação utiliza `jsonschema` em `.tools/python` e os esquemas públicos da Microsoft. O Desktop gravou dez visuais com esquema 2.14 ainda indisponível publicamente; o verificador confere o conteúdo integral desses documentos contra a versão pública 2.5, somente em memória, e identifica essa compatibilidade na saída. O modo `--strict-declared` mantém a falha quando o esquema declarado está indisponível. Nenhuma propriedade ou arquivo nativo é removido para passar a validação.

O resultado final foi de 34 documentos conferidos, com zero falhas: 21 pelo esquema declarado, dez por compatibilidade pública e três descritores pelo esquema público identificado pela extensão. Quatro JSON auxiliares sem esquema estão explicitamente fora dessa contagem. Consulte [a evidência estrutural](docs/validacao_estrutura.json). Essa verificação é distinta da abertura e dos testes de interação efetivamente realizados no Desktop.

## Arquivos entregues

| Caminho | Conteúdo |
|---|---|
| `dashboard/filial_construcao_sc.pbip` e pastas associadas | Projeto Power BI com modelo TMDL e relatório PBIR. |
| `dashboard/dados_snapshot.json` | Agregados públicos exportados da versão SQL identificada. |
| `dashboard/resultados.json` | Resultados calculados e sensibilidade para auditoria. |
| `sql/views_kpis.sql` | Consulta SELECT da fonte SQL utilizada; não cria views nem altera origens. |
| `scripts/build_dashboard.py` | Exportação SQL e geração reproduzível do projeto. |
| `scripts/test_dashboard.py` e `scripts/validate_pbip.py` | Verificações do modelo/estrutura e schemas oficiais. |
| `ETLs/corrigido/` | Coletor corrigido, testes, respostas oficiais e manifesto de cada execução. |
| `docs/` | Método, resultados, design, diagnóstico e checkpoints. |

O backup `DecisaoEstrategica_20261103_081612.backup` é preservado e não foi restaurado. O arquivo `arquivo.sql` contém somente uma consulta; ele não é o backup.

## Limites para uso comercial

O índice retrata indicadores de 2022, com pesos gerenciais e normalização sensível a extremos. Não contém custos, margens, logística, imóveis, raio de influência, obras novas ou projeções de receita. Antes de decidir um investimento, atualizar a concorrência local e realizar estudo financeiro e de demanda. A fonte de rendimento mede trabalho de ocupados com renda, não renda familiar per capita. Unidades locais medem estabelecimentos registrados, não capacidade comercial.

## Publicação e dados locais

O repositório inclui código, projeto Power BI, documentação e agregados municipais públicos do IBGE necessários para abrir e auditar o dashboard. A versão final da coleta é `20261103_135300`; tentativas anteriores de coleta permanecem locais e não são fontes de produção.

Na versão atual e nos novos commits, arquivos `.env`, credenciais, backups do PostgreSQL, chaves privadas, logs, dependências temporárias e caches do Power BI ficam fora do versionamento. `.env.example` contém somente nomes de variáveis com valores vazios. O backup existente permanece local e não é necessário para abrir o relatório. Essas exclusões não removem arquivos de commits antigos; qualquer credencial anteriormente publicada precisa ser trocada, mesmo após excluir o arquivo da versão atual.

Configure as credenciais em arquivo `.env` local para executar coleta/carga ou exportação SQL. Nunca insira valores reais em scripts, documentação, parâmetros versionados ou exemplos. O snapshot do relatório contém apenas agregados públicos; não inclui conexão ativa nem credenciais do banco.
