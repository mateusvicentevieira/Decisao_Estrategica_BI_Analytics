
<div align="center">

# Fontes de Dados e APIs

Documentação das fontes utilizadas para avaliar municípios de Santa Catarina na escolha estratégica de uma nova filial.

<img src="https://img.shields.io/badge/Dados-IBGE-blue?style=for-the-badge" alt="IBGE">
<img src="https://img.shields.io/badge/Emprego-Novo%20CAGED-orange?style=for-the-badge" alt="Novo CAGED">
<img src="https://img.shields.io/badge/Estado-Santa%20Catarina-green?style=for-the-badge" alt="Santa Catarina">

</div>

---

## 1. Mercado

Avalia o tamanho do mercado consumidor e a presença de empresas relacionadas ao setor de construção.

<table>
  <thead>
    <tr>
      <th colspan="2">KPI 01 — Quantidade de Moradores</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Fonte</strong></td>
      <td>IBGE — Censo Demográfico</td>
    </tr>
    <tr>
      <td><strong>Período</strong></td>
      <td>2022</td>
    </tr>
    <tr>
      <td><strong>Nível</strong></td>
      <td>Municipal</td>
    </tr>
    <tr>
      <td><strong>Agregado / Variável</strong></td>
      <td>6750 / 9598</td>
    </tr>
    <tr>
      <td><strong>Filtros</strong></td>
      <td>
        Localidades: <code>N6[N3[42]]</code><br>
        Classificação: <code>2[6794]|86[95251]|14[200]</code>
      </td>
    </tr>
    <tr>
      <td><strong>Endpoint</strong></td>
      <td>
        <a href="https://servicodados.ibge.gov.br/api/v3/agregados/6750/periodos/2022/variaveis/9598?localidades=N6[N3[42]]&classificacao=2[6794]|86[95251]|14[200]">Consultar API do IBGE</a>
      </td>
    </tr>
    <tr>
      <td><strong>Objetivo</strong></td>
      <td>Mensurar a população municipal como indicador do mercado consumidor potencial.</td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <tr>
      <th colspan="2">KPI 02 — Quantidade de Domicílios</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Fonte</strong></td>
      <td>IBGE</td>
    </tr>
    <tr>
      <td><strong>Período</strong></td>
      <td>2022</td>
    </tr>
    <tr>
      <td><strong>Nível</strong></td>
      <td>Municipal</td>
    </tr>
    <tr>
      <td><strong>Agregado / Variável</strong></td>
      <td>6326 / 381</td>
    </tr>
    <tr>
      <td><strong>Filtros</strong></td>
      <td>
        Localidades: <code>N3[42]|N6[N3[42]]</code><br>
        Classificação: <code>125[2932]</code>
      </td>
    </tr>
    <tr>
      <td><strong>Endpoint</strong></td>
      <td>
        <a href="https://servicodados.ibge.gov.br/api/v3/agregados/6326/periodos/2022/variaveis/381?localidades=N3[42]|N6[N3[42]]&classificacao=125[2932]">Consultar API do IBGE</a>
      </td>
    </tr>
    <tr>
      <td><strong>Objetivo</strong></td>
      <td>Estimar o mercado residencial potencial, considerando cada domicílio como uma possível unidade de demanda.</td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <tr>
      <th colspan="2">KPI 03 — Empresas no Setor de Construção</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Fonte</strong></td>
      <td>IBGE</td>
    </tr>
    <tr>
      <td><strong>Período</strong></td>
      <td>2021</td>
    </tr>
    <tr>
      <td><strong>Nível</strong></td>
      <td>Municipal</td>
    </tr>
    <tr>
      <td><strong>Agregado / Variável</strong></td>
      <td>6450 / 706</td>
    </tr>
    <tr>
      <td><strong>Filtros</strong></td>
      <td>
        Localidades: <code>N6[N3[42]]</code><br>
        Classificação: <code>12762[117329,117330,117419,117420,117421,117422,117423,117424,117452,117453,117454,117455,117456]</code>
      </td>
    </tr>
    <tr>
      <td><strong>Endpoint</strong></td>
      <td>
        <a href="https://servicodados.ibge.gov.br/api/v3/agregados/6450/periodos/2021/variaveis/706?localidades=N6[N3[42]]&classificacao=12762[117329,117330,117419,117420,117421,117422,117423,117424,117452,117453,117454,117455,117456]">Consultar API do IBGE</a>
      </td>
    </tr>
    <tr>
      <td><strong>Tratamento</strong></td>
      <td>Separar as categorias retornadas individualmente no SQL e somá-las posteriormente, evitando misturar os valores antes da validação.</td>
    </tr>
  </tbody>
</table>

---

## 2. Poder de Compra

Analisa a renda e a participação da população no mercado de trabalho, além do contingente em idade ativa.

<table>
  <thead>
    <tr>
      <th colspan="2">KPI 04 — Rendimento Mediano</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Fonte</strong></td>
      <td>IBGE</td>
    </tr>
    <tr>
      <td><strong>Período</strong></td>
      <td>2022</td>
    </tr>
    <tr>
      <td><strong>Nível</strong></td>
      <td>Municipal</td>
    </tr>
    <tr>
      <td><strong>Agregado / Variável</strong></td>
      <td>10289 / 13537</td>
    </tr>
    <tr>
      <td><strong>Filtros</strong></td>
      <td>
        Localidades: <code>N6[N3[42]]</code><br>
        Classificação: <code>2[6794]|86[95251]</code>
      </td>
    </tr>
    <tr>
      <td><strong>Endpoint</strong></td>
      <td>
        <a href="https://servicodados.ibge.gov.br/api/v3/agregados/10289/periodos/2022/variaveis/13537?localidades=N6[N3[42]]&classificacao=2[6794]|86[95251]">Consultar API do IBGE</a>
      </td>
    </tr>
    <tr>
      <td><strong>Objetivo</strong></td>
      <td>Avaliar a condição econômica típica do município por meio do rendimento mediano.</td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <tr>
      <th colspan="2">KPI 05 — Taxa de Ocupação</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Fonte</strong></td>
      <td>IBGE — dados de moradores e população em idade ativa</td>
    </tr>
    <tr>
      <td><strong>Período</strong></td>
      <td>2022</td>
    </tr>
    <tr>
      <td><strong>Nível</strong></td>
      <td>Municipal</td>
    </tr>
    <tr>
      <td><strong>Cálculo</strong></td>
      <td>
        <code>(População ocupada / População em idade ativa) × 100</code>
      </td>
    </tr>
    <tr>
      <td><strong>Tratamento</strong></td>
      <td>Somar as faixas etárias necessárias antes de carregar os dados para o banco de dados.</td>
    </tr>
    <tr>
      <td><strong>Observação</strong></td>
      <td>O cálculo depende de uma medida de população ocupada compatível com o período e o universo da população em idade ativa.</td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <tr>
      <th colspan="2">KPI 06 — População em Idade Ativa</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Fonte</strong></td>
      <td>IBGE</td>
    </tr>
    <tr>
      <td><strong>Período</strong></td>
      <td>2022</td>
    </tr>
    <tr>
      <td><strong>Nível</strong></td>
      <td>Municipal</td>
    </tr>
    <tr>
      <td><strong>Agregado / Variável</strong></td>
      <td>6893 / 382</td>
    </tr>
    <tr>
      <td><strong>Filtros</strong></td>
      <td>
        Localidades: <code>N6[N3[42]]</code><br>
        Classificação: <code>125[2932]|58[1143,1144,1145,1146,1147,1148,1149,1150,1151,1152,1153]|86[95251]</code>
      </td>
    </tr>
    <tr>
      <td><strong>Faixa etária</strong></td>
      <td>15 a 69 anos</td>
    </tr>
    <tr>
      <td><strong>Endpoint</strong></td>
      <td>
        <a href="https://servicodados.ibge.gov.br/api/v3/agregados/6893/periodos/2022/variaveis/382?localidades=N6[N3[42]]&classificacao=125[2932]%7C58[1143,1144,1145,1146,1147,1148,1149,1150,1151,1152,1153]%7C86[95251]">Consultar API do IBGE</a>
      </td>
    </tr>
  </tbody>
</table>

---

## 3. Crescimento

Investiga a estrutura etária, a evolução dos domicílios e a movimentação do emprego formal na construção civil.

<table>
  <thead>
    <tr>
      <th colspan="2">KPI 07 — Razão de Dependência</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Fonte</strong></td>
      <td>IBGE</td>
    </tr>
    <tr>
      <td><strong>Período</strong></td>
      <td>2022</td>
    </tr>
    <tr>
      <td><strong>Nível</strong></td>
      <td>Municipal</td>
    </tr>
    <tr>
      <td><strong>Agregado / Variável</strong></td>
      <td>6893 / 382</td>
    </tr>
    <tr>
      <td><strong>Filtros</strong></td>
      <td>
        Localidades: <code>N6[N3[42]]</code><br>
        Classificação: <code>125[2932]|58[1140,1141,1142,1154,1155,6802,6803,92963,92964,92965]|86[95251]</code>
      </td>
    </tr>
    <tr>
      <td><strong>Faixas etárias</strong></td>
      <td>0 a 14 anos e 70 a 100 anos ou mais</td>
    </tr>
    <tr>
      <td><strong>Endpoint</strong></td>
      <td>
        <a href="https://servicodados.ibge.gov.br/api/v3/agregados/6893/periodos/2022/variaveis/382?localidades=N6[N3[42]]&classificacao=125[2932]|58[1140,1141,1142,1154,1155,6802,6803,92963,92964,92965]|86[95251]">Consultar API do IBGE</a>
      </td>
    </tr>
    <tr>
      <td><strong>Interpretação</strong></td>
      <td>Uma menor proporção de população dependente em relação à população em idade ativa tende a indicar menor pressão demográfica sobre esse grupo.</td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <tr>
      <th colspan="2">KPI 08 — Crescimento de Domicílios</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Fonte</strong></td>
      <td>IBGE</td>
    </tr>
    <tr>
      <td><strong>Nível</strong></td>
      <td>Municipal</td>
    </tr>
    <tr>
      <td><strong>Objetivo</strong></td>
      <td>Comparar a evolução da quantidade de domicílios entre os anos censitários disponíveis.</td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <tr>
      <th>Período</th>
      <th>Agregado / Variável</th>
      <th>Filtros</th>
      <th>Endpoint</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>2022</td>
      <td>10053 / 9599</td>
      <td>
        <code>N6[N3[42]]</code><br>
        <code>11558[46292]|14[200]</code>
      </td>
      <td>
        <a href="https://servicodados.ibge.gov.br/api/v3/agregados/10053/periodos/2022/variaveis/9599?localidades=N6[N3[42]]&classificacao=11558[46292]|14[200]" target="_blank" rel="noopener noreferrer">Consultar API</a>
      </td>
    </tr>
    <tr>
      <td>2010</td>
      <td>206 / 96</td>
      <td>
        <code>N6[N3[42]]</code><br>
        <code>1[0]|65[0]</code>
      </td>
      <td>
        <a href="https://servicodados.ibge.gov.br/api/v3/agregados/206/periodos/2010/variaveis/96?localidades=N6[N3[42]]&classificacao=1[0]|65[0]" target="_blank" rel="noopener noreferrer">Consultar API</a>
      </td>
    </tr>
    <tr>
      <td>2000</td>
      <td>206 / 96</td>
      <td>
        <code>N6[N3[42]]</code><br>
        <code>1[0]|65[0]</code>
      </td>
      <td>
        <a href="https://servicodados.ibge.gov.br/api/v3/agregados/206/periodos/2000/variaveis/96?localidades=N6[N3[42]]&classificacao=1[0]|65[0]" target="_blank" rel="noopener noreferrer">Consultar API</a>
      </td>
    </tr>
    <tr>
      <td>1991</td>
      <td>206 / 96</td>
      <td>
        <code>N6[N3[42]]</code><br>
        <code>1[0]|65[0]</code>
      </td>
      <td>
        <a href="https://servicodados.ibge.gov.br/api/v3/agregados/206/periodos/1991/variaveis/96?localidades=N6[N3[42]]&classificacao=1[0]|65[0]" target="_blank" rel="noopener noreferrer">Consultar API</a>
      </td>
    </tr>
    <tr>
      <td>1980</td>
      <td>206 / 96</td>
      <td>
        <code>N6[N3[42]]</code><br>
        <code>1[0]|65[0]</code>
      </td>
      <td>
        <a href="https://servicodados.ibge.gov.br/api/v3/agregados/206/periodos/1980/variaveis/96?localidades=N6[N3[42]]&classificacao=1[0]|65[0]" target="_blank" rel="noopener noreferrer">Consultar API</a>
      </td>
    </tr>
  </tbody>
</table>



<table>
  <thead>
    <tr>
      <th colspan="2">KPI 09 — Admissões e Saldo de Empregos na Construção Civil</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Fonte</strong></td>
      <td>Novo CAGED — Ministério do Trabalho e Emprego</td>
    </tr>
    <tr>
      <td><strong>Período</strong></td>
      <td>Janeiro a agosto de 2026</td>
    </tr>
    <tr>
      <td><strong>Nível</strong></td>
      <td>Municipal</td>
    </tr>
    <tr>
      <td><strong>Dados</strong></td>
      <td>Movimentações de admissões e desligamentos do emprego formal.</td>
    </tr>
    <tr>
      <td><strong>Fonte dos arquivos</strong></td>
      <td>
        <a href="ftp://ftp.mtps.gov.br/pdet/microdados/NOVO%20CAGED/">Acessar microdados do Novo CAGED</a>
      </td>
    </tr>
    <tr>
      <td><strong>Filtros necessários</strong></td>
      <td>
        Filtrar o código IBGE do estado de Santa Catarina e agrupar os dados por município.<br>
        Confirmar também o enquadramento da atividade econômica na construção civil.
      </td>
    </tr>
    <tr>
      <td><strong>Tratamento</strong></td>
      <td>Consolidar as admissões e os desligamentos por município e mês para calcular o saldo de empregos.</td>
    </tr>
    <tr>
      <td><strong>Interpretação</strong></td>
      <td>Saldo positivo indica crescimento líquido do emprego formal no período; saldo negativo indica redução.</td>
    </tr>
  </tbody>
</table>

---

## Tratamento e integração dos dados

- **Extração:** consumir as APIs públicas e baixar os microdados necessários.
- **Padronização:** identificar os municípios pelo código IBGE.
- **Transformação:** validar classificações, somar categorias quando necessário e calcular os indicadores derivados.
- **Armazenamento:** carregar os dados tratados no PostgreSQL.
- **Visualização:** utilizar o Power BI para comparar os municípios e apoiar a decisão estratégica.

<div align="center">
  <sub>Projeto de portfólio — Business Intelligence e análise de dados para seleção de municípios em Santa Catarina.</sub>
</div>
