import unittest
from layers.l2_ego import L2Laws


class TestL2Laws(unittest.TestCase):
    def setUp(self):
        self.l2 = L2Laws()

    def test_alpha_beta_conservation(self):
        ok, reason = self.l2.conservacion_alpha_beta(None, None, {})
        self.assertTrue(ok)
        self.assertEqual(reason, "PASS")

    def test_beta_irreducibility(self):
        ok, reason = self.l2.irreducibilidad_beta(None, None, {})
        self.assertTrue(ok)
        self.assertEqual(reason, "PASS")

    def test_vpsi_pass_with_memory_hits(self):
        context = {"memory_hits": ["doc1"], "derived": False}
        ok, reason = self.l2.vpsi_check(
            output="beta se conecta con estructura",
            inputs="beta estructura",
            context=context,
        )
        self.assertTrue(ok)
        self.assertEqual(reason, "PASS")

    def test_vpsi_pass_with_derived_flag(self):
        context = {"memory_hits": [], "derived": True}
        ok, reason = self.l2.vpsi_check(
            output="salida derivada",
            inputs="entrada",
            context=context,
        )
        self.assertTrue(ok)
        self.assertEqual(reason, "PASS")

    def test_vpsi_fail_when_not_derivable(self):
        context = {"memory_hits": [], "derived": False}
        ok, reason = self.l2.vpsi_check(
            output="contenido totalmente externo",
            inputs="beta estructura",
            context=context,
        )
        self.assertFalse(ok)
        self.assertEqual(reason, "la salida no es derivable de los operandos")

    def test_ley_1_accion_fails_without_input(self):
        ok, reason = self.l2.ley_1_accion(
            output="algo",
            inputs="",
            context={},
        )
        self.assertFalse(ok)
        self.assertEqual(reason, "no hay input real que active el sistema")

    def test_ley_2_ritmo_pass_with_trace(self):
        context = {"trace": ["input->memory", "memory->output"]}
        ok, reason = self.l2.ley_2_ritmo(
            output="algo",
            inputs="entrada",
            context=context,
        )
        self.assertTrue(ok)
        self.assertEqual(reason, "PASS")

    def test_ley_2_ritmo_fail_without_trace(self):
        context = {"trace": []}
        ok, reason = self.l2.ley_2_ritmo(
            output="algo",
            inputs="entrada",
            context=context,
        )
        self.assertFalse(ok)
        self.assertEqual(reason, "no hay secuencia trazable de procesamiento")

    def test_ley_4_causa_efecto_fail_without_support(self):
        context = {"supported": False}
        ok, reason = self.l2.ley_4_causa_efecto(
            output="afirmacion",
            inputs="entrada",
            context=context,
        )
        self.assertFalse(ok)
        self.assertEqual(reason, "hay afirmaciones sin causa o soporte")

    def test_validate_pass_complete_context(self):
        context = {
            "memory_hits": ["doc_beta"],
            "derived": True,
            "trace": ["input->memory", "memory->association", "association->output"],
            "supported": True,
            "integrated": True,
            "fractal_consistent": True,
            "resonant": True,
            "polarity_checked": True,
            "total_integration": True,
        }

        ok, violations = self.l2.validate(
            output="beta conecta estructura con memoria",
            inputs="beta memoria estructura",
            context=context,
        )
        self.assertTrue(ok)
        self.assertEqual(violations, [])

    def test_validate_fail_incomplete_context(self):
        context = {
            "memory_hits": [],
            "derived": False,
            "trace": [],
            "supported": False,
            "integrated": False,
            "fractal_consistent": False,
            "resonant": False,
            "polarity_checked": False,
            "total_integration": False,
        }

        ok, violations = self.l2.validate(
            output="salida no trazable",
            inputs="entrada minima",
            context=context,
        )
        self.assertFalse(ok)
        self.assertGreater(len(violations), 0)


if __name__ == "__main__":
    unittest.main()