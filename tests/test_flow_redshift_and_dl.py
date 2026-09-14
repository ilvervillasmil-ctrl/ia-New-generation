import math

# Usa tus constantes del framework (ajusta el import si tu repo usa otra ruta)
from core.constants import BETA, PHI


def lambda_omega() -> float:
    """Tu fórmula: ΛΩ = β^(27π + β φ^2)"""
    exponent = 27.0 * math.pi + BETA * (PHI ** 2)
    return BETA ** exponent


def h0_from_lambda(L: float, omega_lambda: float = 0.685) -> float:
    """
    En unidades de Planck (c=1):
    Λ = 3 ΩΛ H0^2  =>  H0 = sqrt(Λ / (3 ΩΛ))
    """
    return math.sqrt(L / (3.0 * omega_lambda))


def simpson_integral(f, a: float, b: float, n: int = 4000) -> float:
    """Integración numérica simple (Simpson). n debe ser par."""
    if n % 2 == 1:
        n += 1
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        x = a + i * h
        s += (4 if i % 2 == 1 else 2) * f(x)
    return s * h / 3.0


def e_z(z: float, omega_lambda: float = 0.685) -> float:
    """
    Modelo mínimo tipo FLRW plano para d_L:
    E(z)=H(z)/H0 = sqrt(Ωm(1+z)^3 + ΩΛ), con Ωm = 1-ΩΛ
    """
    omega_m = 1.0 - omega_lambda
    return math.sqrt(omega_m * (1.0 + z) ** 3 + omega_lambda)


def luminosity_distance(z: float, omega_lambda: float = 0.685) -> float:
    """
    d_L(z) = (1+z) * ∫_0^z dz' / H(z')
          = (1+z) * (1/H0) * ∫_0^z dz' / E(z')
    (c=1 en Planck units)
    """
    L = lambda_omega()
    H0 = h0_from_lambda(L, omega_lambda=omega_lambda)
    I = simpson_integral(lambda zz: 1.0 / e_z(zz, omega_lambda=omega_lambda), 0.0, z)
    return (1.0 + z) * (I / H0)


class TestFlowRedshiftAndDL:
    def test_lambda_omega_value_order(self):
        L = lambda_omega()
        # Debe estar ~1e-122 en Planck units
        assert 1e-123 < L < 1e-121

    def test_h0_reconstruction_reasonable(self):
        L = lambda_omega()
        H0 = h0_from_lambda(L, omega_lambda=0.685)
        # Orden esperado ~1e-61 en Planck units
        assert 1e-62 < H0 < 1e-60

    def test_dL_zero_is_zero(self):
        assert abs(luminosity_distance(0.0)) < 1e-15

    def test_dL_monotonic_in_z(self):
        zs = [0.01, 0.05, 0.1, 0.3, 0.6, 1.0]
        ds = [luminosity_distance(z) for z in zs]
        assert all(ds[i] < ds[i + 1] for i in range(len(ds) - 1))

    def test_small_z_hubble_limit(self):
        """
        Límite z<<1:
        d_L(z) ≈ z/H0  (porque (1+z)≈1 y E(z)≈1)
        Esto es tu ecuación mínima de redshift↔distancia en régimen pequeño.
        """
        z = 1e-3
        L = lambda_omega()
        H0 = h0_from_lambda(L, omega_lambda=0.685)

        dL = luminosity_distance(z, omega_lambda=0.685)
        approx = z / H0

        rel_err = abs(dL - approx) / approx
        assert rel_err < 0.02  # 2% de tolerancia numérica

    def test_redshift_from_distance_small_z(self):
        """
        Ecuación mínima (aprox) del modelo de flujo en bajo-z:
        z ≈ H0 * d  (con c=1)
        La probamos usando d ≈ d_L/(1+z) ≈ d_L cuando z es pequeño.
        """
        z = 1e-3
        L = lambda_omega()
        H0 = h0_from_lambda(L, omega_lambda=0.685)

        dL = luminosity_distance(z, omega_lambda=0.685)
        z_hat = H0 * dL

        rel_err = abs(z_hat - z) / z
        assert rel_err < 0.02
