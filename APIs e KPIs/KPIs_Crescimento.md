
<h1 align="center">KPIs — Crescimento</h1>

<p align="center">
  Indicadores para avaliar a expansão demográfica e o dinamismo
  do setor da construção nos municípios de Santa Catarina.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Área-Crescimento-1565C0?style=flat-square">
  <img src="https://img.shields.io/badge/Granularidade-Município-607D8B?style=flat-square">
  <img src="https://img.shields.io/badge/Status-Em%20desenvolvimento-blue?style=flat-square">
</p>

---

## Como o crescimento será avaliado?

<table>
  <tr>
    <td align="center" width="33%">
      <img src="https://img.icons8.com/fluency/96/family.png"
           width="55" alt="Razão de Dependência">
      <h3>05. Razão de Dependência</h3>
      <p>Relação entre a população dependente e a população em idade ativa.</p>
      <strong>Menor é melhor</strong>
    </td>
    <td align="center" width="33%">
      <img src="https://img.icons8.com/fluency/96/home.png"
           width="55" alt="Crescimento de Domicílios">
      <h3>06. Crescimento de Domicílios</h3>
      <p>Variação da quantidade de domicílios ao longo do tempo.</p>
      <strong>Maior é melhor</strong>
    </td>
    <td align="center" width="33%">
      <img src="https://img.icons8.com/fluency/96/under-construction.png"
           width="55" alt="Construção Civil">
      <h3>07. Intensidade de Novas Construções</h3>
      <p>Movimentação formal de empregos no setor da construção.</p>
      <strong>Maior saldo é melhor</strong>
    </td>
  </tr>
</table>

---

<h2>05. Razão de Dependência</h2>

<table>
  <tr>
    <td width="70%">
      <h3>O que esse indicador mede?</h3>
      A relação entre a população potencialmente dependente
      e a população em idade potencialmente ativa.
      <br><br>
      <strong>Objetivo:</strong> compreender a estrutura etária
      de cada município.
    </td>
    <td align="center" width="30%">
      <img src="https://img.icons8.com/fluency/96/family.png"
           width="75" alt="Razão de Dependência">
    </td>
  </tr>
</table>

<h3>Por que utilizar?</h3>

Uma proporção maior de crianças e idosos em relação à população
em idade ativa pode indicar uma estrutura demográfica diferente.
O indicador ajudará a contextualizar o perfil de cada município.

<h3>Como será calculado?</h3>

<table>
  <tr>
    <td align="center">
      <strong>Razão de Dependência (%)</strong>
      <br><br>
      População Dependente ÷ População em Idade Ativa × 100
    </td>
  </tr>
</table>

<h3>Como entra na análise?</h3>

<ul>
  <li>Sua inclusão definitiva no modelo ainda será avaliada.</li>
  <li>Se aprovado, será convertido em um score de 0 a 100.</li>
  <li>A pontuação terá direção inversa: uma razão menor será
      considerada mais favorável.</li>
</ul>

<table>
  <tr>
    <td width="30%"><strong>Fonte</strong></td>
    <td>IBGE — Censo Demográfico</td>
  </tr>
  <tr>
    <td><strong>Período</strong></td>
    <td>2022</td>
  </tr>
  <tr>
    <td><strong>Granularidade</strong></td>
    <td>Município</td>
  </tr>
</table>

---

<h2>06. Crescimento de Domicílios</h2>

<table>
  <tr>
    <td width="70%">
      <h3>O que esse indicador mede?</h3>
      A variação percentual da quantidade de domicílios entre
      dois períodos.
      <br><br>
      <strong>Objetivo:</strong> identificar municípios onde
      o mercado residencial está se expandindo.
    </td>
    <td align="center" width="30%">
      <img src="https://img.icons8.com/fluency/96/home.png"
           width="75" alt="Crescimento de Domicílios">
    </td>
  </tr>
</table>

<h3>Por que utilizar?</h3>

O crescimento de domicílios ajuda a identificar a expansão
da demanda potencial por construção, reformas, acabamentos
e manutenção.

Diferentemente da quantidade total de domicílios, este indicador
mostra como o mercado residencial mudou ao longo do tempo.

<h3>Como será calculado?</h3>

<table>
  <tr>
    <td align="center">
      <strong>Crescimento de Domicílios (%)</strong>
      <br><br>
      (Domicílios do período atual − Domicílios do período anterior)
      ÷ Domicílios do período anterior × 100
    </td>
  </tr>
</table>

<h3>Como entra na análise?</h3>

<ul>
  <li>Será convertido em um score de 0 a 100.</li>
  <li>Receberá o peso definido para o nível de Crescimento.</li>
  <li>Quanto maior o crescimento, maior o potencial de expansão
      do mercado residencial.</li>
</ul>

<table>
  <tr>
    <td width="30%"><strong>Fonte</strong></td>
    <td>IBGE — Censo Demográfico</td>
  </tr>
  <tr>
    <td><strong>Período</strong></td>
    <td>1980–2022</td>
  </tr>
  <tr>
    <td><strong>Granularidade</strong></td>
    <td>Município</td>
  </tr>
</table>

---

<h2>07. Intensidade de Novas Construções</h2>

<table>
  <tr>
    <td width="70%">
      <h3>O que esse indicador mede?</h3>
      O saldo de admissões e desligamentos formais no setor
      da construção civil.
      <br><br>
      <strong>Objetivo:</strong> avaliar o dinamismo recente
      do setor nos municípios.
    </td>
    <td align="center" width="30%">
      <img src="https://img.icons8.com/fluency/96/under-construction.png"
           width="75" alt="Construção Civil">
    </td>
  </tr>
</table>

<h3>Por que utilizar?</h3>

O indicador busca aproximar a análise da atividade recente
da construção civil.

Enquanto a quantidade e o crescimento de domicílios mostram
o tamanho e a expansão do mercado residencial, a movimentação
de empregos ajuda a observar mudanças recentes na atividade formal.

<strong>Atenção:</strong> o saldo de empregos é uma proxy do dinamismo
do setor. Ele não mede diretamente a quantidade de obras, o volume
de materiais consumidos ou o faturamento das empresas.

<h3>Como será calculado?</h3>

<table>
  <tr>
    <td align="center">
      <strong>Saldo de Empregos da Construção Civil</strong>
      <br><br>
      Admissões formais − Desligamentos formais
      <br><br>
      <sub>Filtro previsto: Seção F da CNAE 2.0.</sub>
    </td>
  </tr>
</table>

<h3>Como entra na análise?</h3>

<ul>
  <li>Serão considerados os últimos 12 meses disponíveis.</li>
  <li>O saldo municipal será convertido em score de 0 a 100
      por normalização Min-Max.</li>
  <li>O score será utilizado conforme o peso definido para
      o nível de Crescimento.</li>
  <li>Um saldo maior será considerado mais favorável dentro
      deste indicador.</li>
</ul>

<table>
  <tr>
    <td width="30%"><strong>Fonte</strong></td>
    <td>Ministério do Trabalho e Emprego (MTE) — PDET / Novo CAGED</td>
  </tr>
  <tr>
    <td><strong>Período</strong></td>
    <td>Acumulado dos últimos 12 meses disponíveis</td>
  </tr>
  <tr>
    <td><strong>Classificação</strong></td>
    <td>CNAE 2.0 — Seção F: Construção</td>
  </tr>
  <tr>
    <td><strong>Granularidade</strong></td>
    <td>Município</td>
  </tr>
</table>

---

<h2>Como os indicadores serão utilizados?</h2>

<table>
  <tr>
    <td align="center" width="33%">
      <img src="https://img.icons8.com/fluency/96/database.png"
           width="50" alt="Coleta de dados">
      <h3>1. Coleta</h3>
      <p>Reunir dados demográficos e do mercado de trabalho.</p>
    </td>
    <td align="center" width="33%">
      <img src="https://img.icons8.com/fluency/96/combo-chart.png"
           width="50" alt="Pontuação">
      <h3>2. Pontuação</h3>
      <p>Padronizar os indicadores em scores de 0 a 100,
      respeitando a direção de cada KPI.</p>
    </td>
    <td align="center" width="33%">
      <img src="https://img.icons8.com/fluency/96/graph.png"
           width="50" alt="Comparação">
      <h3>3. Comparação</h3>
      <p>Comparar os municípios e avaliar seu potencial de crescimento.</p>
    </td>
  </tr>
</table>

---

<div align="center">
  <img src="https://img.shields.io/badge/Projeto-Decisão%20Estratégica-1565C0?style=for-the-badge">
  <p><strong>Dados para apoiar decisões de expansão.</strong></p>
  <sub>KPIs de Crescimento | Em desenvolvimento</sub>
</div>
```

