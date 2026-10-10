<h1 align="center">KPIs — Mercado</h1>

<p align="center">
  Indicadores para avaliar o potencial de mercado dos municípios
  de Santa Catarina para a abertura de uma nova filial.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Área-Mercado-1565C0?style=flat-square">
  <img src="https://img.shields.io/badge/Fonte-IBGE%20e%20CEMPRE-2E7D32?style=flat-square">
  <img src="https://img.shields.io/badge/Granularidade-Município-607D8B?style=flat-square">
</p>

---

## Como o mercado será avaliado?

A análise considera três indicadores: população, quantidade de
domicílios e empresas relacionadas ao setor de construção.

<table>
  <tr>
    <td align="center" width="33%">
      <img src="https://img.icons8.com/fluency/96/conference.png"
           width="55" alt="População">
      <h3>01. População</h3>
      <p>Tamanho do mercado consumidor.</p>
      <strong>Peso: 40%</strong>
    </td>
    <td align="center" width="33%">
      <img src="https://img.icons8.com/fluency/96/home.png"
           width="55" alt="Domicílios">
      <h3>02. Domicílios</h3>
      <p>Quantidade de unidades que podem demandar produtos.</p>
      <strong>Peso: 60%</strong>
    </td>
    <td align="center" width="33%">
      <img src="https://img.icons8.com/fluency/96/shop.png"
           width="55" alt="Empresas">
      <h3>03. Empresas</h3>
      <p>Potencial de demanda do mercado profissional.</p>
      <strong>Peso: A definir</strong>
    </td>
  </tr>
</table>

<p align="center">
  <sub>Os pesos de população e domicílios correspondem à composição
  do mercado residencial. O peso do terceiro indicador ainda não foi definido.</sub>
</p>

---

## 01. População

<img src="https://img.icons8.com/fluency/96/conference.png"
     width="55" alt="População">

**O que mede?**

A quantidade de habitantes de cada município.

**Por que analisar?**

Ajuda a estimar o tamanho potencial do mercado consumidor.
Entretanto, população não significa quantidade de clientes,
pois várias pessoas podem morar na mesma residência e compartilhar
as decisões de compra.

**Como será calculado?**

População = quantidade de habitantes do município


**Como entra na análise?**

- Será convertida em um score de 0 a 100.
- Terá peso de 40% dentro do mercado residencial.
- Quanto maior a população, maior o potencial indicado pelo KPI.

| Informação | Detalhe |
|---|---|
| Fonte | IBGE — Censo Demográfico |
| Período | 2022 |
| Granularidade | Município |

---

## 02. Domicílios

<img src="https://img.icons8.com/fluency/96/home.png"
     width="55" alt="Domicílios">

**O que mede?**

A quantidade de domicílios existentes em cada município.

**Por que analisar?**

Cada domicílio representa uma unidade física que pode precisar
de materiais de construção e manutenção, independentemente
da quantidade de moradores.

**Como será calculado?**

```text
Domicílios = quantidade de domicílios existentes no município
```

**Como entra na análise?**

- Será convertido em um score de 0 a 100.
- Terá peso de 60% dentro do mercado residencial.
- Quanto maior a quantidade de domicílios, maior o potencial
  indicado pelo KPI.

| Informação | Detalhe |
|---|---|
| Fonte | IBGE — Censo Demográfico |
| Período | 2022 |
| Granularidade | Município |

---

## 03. Empresas relacionadas à construção

<img src="https://img.icons8.com/fluency/96/shop.png"
     width="55" alt="Empresas">

**O que mede?**

A quantidade de empresas relacionadas às atividades econômicas
de venda de materiais de construção em cada município.

**Por que analisar?**

Ajuda a estimar o potencial de demanda de empresas e profissionais
que atuam no mercado da construção.

**Atenção:** este indicador é uma *proxy*. A quantidade de empresas
não representa diretamente o faturamento nem o volume de compras.

**Como será calculado?**

```text
Empresas = quantidade de empresas enquadradas
nas atividades econômicas selecionadas
```

A classificação econômica exata ainda será definida durante
o desenvolvimento do projeto.

**Como entra na análise?**

- Quanto maior a quantidade de empresas, maior o potencial
  indicado pelo KPI.
- A regra de pontuação e o peso ainda serão definidos.

| Informação | Detalhe |
|---|---|
| Fonte | Cadastro Central de Empresas (CEMPRE) |
| Período | 2021 |
| Granularidade | Município |
| Classificação prevista | Empresas especializadas em vendas por atacado e varejo de materiais de construção |

---

## Como os indicadores serão utilizados?

<div align="center">

  <img src="https://img.icons8.com/fluency/96/database.png"
       width="45" alt="Dados">

  <h3>Dados municipais</h3>
  <p>Coleta das informações nas fontes públicas.</p>

  <img src="https://img.icons8.com/fluency/96/combo-chart.png"
       width="45" alt="Pontuação">

  <h3>Padronização dos indicadores</h3>
  <p>Conversão dos valores em scores de 0 a 100,
  conforme as regras que serão definidas.</p>

  <img src="https://img.icons8.com/fluency/96/graph.png"
       width="45" alt="Comparação">

  <h3>Comparação dos municípios</h3>
  <p>Análise dos resultados para identificar
  os mercados com maior potencial.</p>

</div>

---

<div align="center">
  <img src="https://img.shields.io/badge/Projeto-Decisão%20Estratégica-1565C0?style=for-the-badge">
  <p><strong>Dados para apoiar decisões de expansão.</strong></p>
  <sub>Documentação dos KPIs de Mercado | Em desenvolvimento</sub>
</div>
