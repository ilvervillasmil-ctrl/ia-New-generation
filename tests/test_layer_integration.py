# tests/test_layer_integration.py

import pytest
from layers.l7_integration import LayerIntegration
from formulas.constants import ALPHA, BETA


class TestLayerIntegration:
    """
    L7 = producto multiplicativo de L0-L6.
    L6 orienta. L7 verifica.
    Todo lo que no se integra colapsa.
    """

    def _full_layers(self, L=1.0, phi=0.0):
        return [{'L': L, 'phi': phi}] * 7

    def test_L7_is_emergent_not_declared(self):
        """L7 no se declara. Se calcula."""
        layer = LayerIntegration()
        assert layer.value == 0.0

    def test_L7_full_activation_no_friction(self):
        """L=1, phi=0 en todas: L7 clamped a ALPHA."""
        layer  = LayerIntegration()
        result = layer.compute(self._full_layers(L=1.0, phi=0.0))
        assert result == pytest.approx(ALPHA, rel=1e-10)

    def test_L7_collapses_if_any_layer_zero(self):
        """Si cualquier L=0, L7=0. Sin excepciones."""
        for i in range(7):
            layers    = self._full_layers(L=1.0, phi=0.0)
            layers[i] = {'L': 0.0, 'phi': 0.0}
            layer     = LayerIntegration()
            result    = layer.compute(layers)
            assert result == 0.0, (
                f"L{i}=0 debe colapsar L7"
            )

    def test_L7_collapses_if_any_friction_full(self):
        """Si phi=1 en cualquier capa, L7=0."""
        for i in range(7):
            layers    = self._full_layers(L=1.0, phi=0.0)
            layers[i] = {'L': 1.0, 'phi': 1.0}
            layer     = LayerIntegration()
            result    = layer.compute(layers)
            assert result == 0.0, (
                f"L{i}.phi=1 debe colapsar L7"
            )

    def test_L6_perfect_but_L3_collapsed_L7_is_zero(self):
        """
        L6 puede estar perfectamente orientada
        pero si L3 falla, L7 = 0.
        L6 orienta. L7 verifica.
        """
        layers    = self._full_layers(L=1.0, phi=0.0)
        layers[6] = {'L': 1.0, 'phi': 0.0}  # L6 perfecta
        layers[3] = {'L': 0.0, 'phi': 0.0}  # L3 colapsada

        layer  = LayerIntegration()
        result = layer.compute(layers)

        assert result == 0.0, (
            "L6=1 no salva el sistema si L3=0. "
            "L6 orienta, L7 verifica."
        )

    def test_L7_never_exceeds_alpha(self):
        """L7 nunca puede superar ALPHA. Beta es irreducible."""
        layer  = LayerIntegration()
        result = layer.compute(self._full_layers(L=1.0, phi=0.0))
        assert result <= ALPHA
        assert result < 1.0

    def test_L7_never_negative(self):
        """L7 >= 0 siempre."""
        layer  = LayerIntegration()
        result = layer.compute(self._full_layers(L=0.5, phi=0.3))
        assert result >= 0.0

    def test_is_integrated_false_when_zero(self):
        """is_integrated() = False si L7=0."""
        layers    = self._full_layers(L=1.0, phi=0.0)
        layers[0] = {'L': 0.0, 'phi': 0.0}
        layer     = LayerIntegration()
        layer.compute(layers)
        assert not layer.is_integrated()

    def test_is_integrated_true_when_positive(self):
        """is_integrated() = True si todas las capas cooperan."""
        layer = LayerIntegration()
        layer.compute(self._full_layers(L=1.0, phi=0.0))
        assert layer.is_integrated()

    def test_requires_exactly_7_layers(self):
        """L7 requiere exactamente 7 capas -- L0 a L6."""
        layer = LayerIntegration()
        with pytest.raises(ValueError):
            layer.compute(self._full_layers()[:6])

    def test_multiplicative_structure_exact(self):
        """
        Verificacion del producto exacto.
        L=[0.8, 0.9, 1.0, 0.95, 0.85, 0.9, 1.0]
        phi=[0.1, 0.05, 0.02, 0.01, 0.03, 0.02, 0.0]
        """
        layers = [
            {'L': 0.8,  'phi': 0.10},
            {'L': 0.9,  'phi': 0.05},
            {'L': 1.0,  'phi': 0.02},
            {'L': 0.95, 'phi': 0.01},
            {'L': 0.85, 'phi': 0.03},
            {'L': 0.9,  'phi': 0.02},
            {'L': 1.0,  'phi': 0.00},
        ]
        expected = 1.0
        for l in layers:
            expected *= l['L'] * (1 - l['phi'])
        expected = min(ALPHA, expected)

        layer  = LayerIntegration()
        result = layer.compute(layers)
        assert result == pytest.approx(expected, rel=1e-10)

    def test_export_structure(self):
        """export() retorna dict con L, phi, name."""
        layer = LayerIntegration()
        layer.compute(self._full_layers(L=1.0, phi=0.0))
        exported = layer.export()
        assert 'L'    in exported
        assert 'phi'  in exported
        assert 'name' in exported
        assert exported['phi']  == 0.0
        assert exported['name'] == "Integration"
        assert exported['L']    == layer.value
