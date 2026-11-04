-- Consulta somente leitura; não altera tabelas de origem.
-- Todos os dados incorporados no PBIP são exportados desta fonte.
SELECT * FROM bi_validado.fontes_20261103_135300 ORDER BY id_municipio,kpi,periodo;
