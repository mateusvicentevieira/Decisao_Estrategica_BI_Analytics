"""Contratos de exportação e normalização; fixtures pequenas, não dados do relatório."""
import unittest
import json
import re
from build_dashboard import normalize, weighted_index, m_value, validate_records, numeric, ROOT, REPORT, MODEL


class DashboardTests(unittest.TestCase):
    def test_missing_is_not_zero(self):
        self.assertEqual(normalize([None, 10, 30]), [None, 0.0, 100.0])

    def test_constant_cannot_create_score(self):
        self.assertEqual(normalize([3, 3]), [None, None])

    def test_competition_direction_is_inverted(self):
        self.assertEqual(normalize([1, 3, 5], reverse=True), [100.0, 50.0, 0.0])

    def test_incomplete_index_stays_missing(self):
        self.assertIsNone(weighted_index([100, None, 50, 50], [40, 30, 20, 10]))
        self.assertAlmostEqual(weighted_index([100, 0, 50, 50], [40, 30, 20, 10]), 55)

    def test_wrong_year_and_duplicate_source_rejected(self):
        row = {'id_municipio':'4200051', 'kpi':'renda', 'periodo':2022}
        with self.assertRaises(ValueError):
            validate_records([row, row])
        with self.assertRaises(ValueError):
            validate_records([dict(row, periodo=2021)])

    def test_powerquery_string_quotes_and_null(self):
        self.assertEqual(m_value('a"b'), '"a""b"')
        self.assertEqual(m_value(None), 'null')

    def test_desktop_font_values_require_typed_numeric_literal(self):
        # Regressão observada no Desktop: "12" é descartado; "12D" aplica fonte12.
        self.assertEqual(numeric(12), {'expr':{'Literal':{'Value':'12D'}}})
        self.assertEqual(numeric(1,'L'), {'expr':{'Literal':{'Value':'1L'}}})

    def test_generated_visual_references_resolve_to_model_fields(self):
        if not MODEL.exists():self.skipTest('Execute build_dashboard.py para verificar artefatos reais')
        fields={}
        for path in (MODEL/'definition/tables').glob('*.tmdl'):
            text=path.read_text(encoding='utf-8')
            names=re.findall(r"^\t(?:column|measure) (?:'([^']+)'|([^\s=]+))",text,re.M)
            actual=[a or b for a,b in names]
            self.assertEqual(len(actual),len(set(n.casefold() for n in actual)),f'Colisão de nomes em {path.name}')
            fields[path.stem]=set(actual)
        for path in REPORT.rglob('visual.json'):
            v=json.loads(path.read_text(encoding='utf-8'))
            for state in v['visual'].get('query',{}).get('queryState',{}).values():
                for projection in state['projections']:
                    f=next(iter(projection['field'].values()))
                    self.assertIn(f['Property'],fields[f['Expression']['SourceRef']['Entity']],str(path))

    def test_two_pages_and_name_slicer_are_present(self):
        if not REPORT.exists():self.skipTest('Execute build_dashboard.py para verificar artefatos reais')
        self.assertEqual(len(list((REPORT/'definition/pages').glob('*/page.json'))),2)
        slicer=REPORT/'definition/pages/analise_municipio/visuals/municipio/visual.json'
        v=json.loads(slicer.read_text(encoding='utf-8'))
        self.assertEqual(v['visual']['visualType'],'slicer')
        self.assertEqual(v['visual']['query']['queryState']['Values']['projections'][0]['field']['Column']['Property'],'municipio')


if __name__ == '__main__':
    unittest.main()
