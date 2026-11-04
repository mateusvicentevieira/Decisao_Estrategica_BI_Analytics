import unittest
from coletor import numero, validar_categorias, alinhar_periodos, validar_cobertura, agregar_exclusivas, movimento_construcao


class Integridade(unittest.TestCase):
    def test_ausencia_nao_vira_zero(self):
        for valor in (None, '', '...', '..', 'X'):
            self.assertIsNone(numero(valor))
        self.assertEqual(numero('-'), 0)
        self.assertEqual(numero('0'), 0)
        self.assertEqual(numero('-12'), -12)

    def test_nao_finitos_sao_rejeitados(self):
        for valor in ('NaN', 'Infinity', '-Infinity'):
            self.assertIsNone(numero(valor))

    def test_periodos_vazios_erro_explicito(self):
        with self.assertRaises(ValueError):
            alinhar_periodos([])

    def test_pai_e_filho_sao_rejeitados(self):
        with self.assertRaises(ValueError):
            validar_categorias(['47.4', '47.41-5'])
        validar_categorias(['47.41-5', '47.42-3'])

    def test_periodos_diferentes_nao_entram_na_formula(self):
        with self.assertRaises(ValueError):
            alinhar_periodos([2021, 2022])
        self.assertEqual(alinhar_periodos([2022, 2022]), 2022)

    def test_cobertura_e_duplicatas(self):
        with self.assertRaises(ValueError):
            validar_cobertura(['4200051'], {'4200051','4200101'})
        with self.assertRaises(ValueError):
            validar_cobertura(['4200051','4200051'], {'4200051'})
        validar_cobertura(['4200051','4200101'], {'4200051','4200101'})

    def test_soma_exclusiva_preserva_incompletude(self):
        self.assertEqual(agregar_exclusivas([('47.41-5', 5),('47.42-3', 7)]),12)
        self.assertIsNone(agregar_exclusivas([('47.41-5', 5),('47.42-3', None)]))
        with self.assertRaises(ValueError):
            agregar_exclusivas([('47.4', 12),('47.41-5', 5)])

    def test_caged_somente_secao_f(self):
        self.assertTrue(movimento_construcao({'secao':'F'}))
        self.assertTrue(movimento_construcao({'subclasse':'4120400'}))
        self.assertFalse(movimento_construcao({'secao':'G','subclasse':'4744001'}))
        with self.assertRaises(ValueError):
            movimento_construcao({})


if __name__ == '__main__':
    unittest.main()
