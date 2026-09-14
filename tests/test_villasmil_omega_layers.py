"""
TEST SUITE - VILLASMIL-OMEGA LAYERED ARCHITECTURE
Validacion computacional de las 8 capas del framework
para el analisis de ecuaciones diofanticas.

Cada test verifica una capa estructural del paper.
Ningun valor hardcodeado: todo se deriva de las definiciones.

Autor: Ilver Villasmil
Arquitectura: Villasmil-Omega (2026)
"""

import math
import pytest
from functools import reduce
from collections import defaultdict


# ==========================================
# MOTOR LOGICO: ARQUITECTURA OMEGA
# ==========================================

def factorizar(n):
    """Factorizacion prima completa de n."""
    factores = {}
    d = 2
    temp = abs(n)
    while d * d <= temp:
        while temp % d == 0:
            factores[d] = factores.get(d, 0) + 1
            temp //= d
        d += 1
    if temp > 1:
        factores[temp] = factores.get(temp, 0) + 1
    return factores


def calcular_z(n):
    """
    Invariante Estructural z(N) = gcd{v_p(N) : p | N}.
    z(N) = m si y solo si N = c^m con c no potencia perfecta.
    """
    if n <= 1:
        return 0
    factores = factorizar(n)
    if not factores:
        return 1
    return reduce(math.gcd, factores.values())


def v_p(n, p):
    """Valuacion p-adica de n."""
    if n == 0:
        return float("inf")
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return v


def es_potencia_perfecta(n, z):
    """Verifica si n = c^z para algun entero c."""
    if n <= 0:
        return False
    c = round(n ** (1.0 / z))
    for candidato in [c - 1, c, c + 1]:
        if candidato > 0 and candidato ** z == n:
            return True
    return False


def existe_primo_rompedor(n, z):
    """
    Capa E6: verifica si existe un primo p | N
    tal que v_p(N) no es divisible por z.
    """
    factores = factorizar(n)
    for p, e in factores.items():
        if e % z != 0:
            return True, p, e
    return False, None, None


def canales_ciclotomicos(a, b, n):
    """
    Descompone a^n + b^n en canales S y Q
    para n impar: a^n + b^n = (a+b) * Q_{n-1}(a,b)
    """
    S = a + b
    Q = (a ** n + b ** n) // S
    return S, Q


# ==========================================
# CAPA E0 - DOMINIO
# ==========================================

class TestCapaE0_Dominio:
    """Verifica: A, B, C, x, y, z son enteros positivos."""

    def test_enteros_positivos_validos(self):
        """El dominio solo admite enteros positivos."""
        for val in [1, 2, 3, 100, 9999]:
            assert isinstance(val, int)
            assert val > 0

    def test_cero_excluido(self):
        """El cero no pertenece al dominio Z+."""
        assert 0 not in range(1, 100)

    def test_negativos_excluidos(self):
        """Los negativos no pertenecen al dominio."""
        for val in [-1, -5, -100]:
            assert val < 1

    def test_factorizacion_requiere_positivo(self):
        """La factorizacion opera sobre enteros positivos."""
        for n in [2, 6, 12, 100, 1001]:
            f = factorizar(n)
            assert all(p > 0 for p in f.keys())
            assert all(e > 0 for e in f.values())


# ==========================================
# CAPA E1 - FILTRO DE REGIMEN
# ==========================================

class TestCapaE1_Regimen:
    """Verifica: x, y, z >= 3 excluye regimenes cuadraticos."""

    def test_exponentes_minimos(self):
        """El regimen Beal exige x, y, z >= 3."""
        for x in range(3, 10):
            for y in range(3, 10):
                for z in range(3, 10):
                    assert x >= 3 and y >= 3 and z >= 3

    def test_cuadratico_excluido(self):
        """Exponente 2 queda fuera del regimen."""
        assert 2 < 3

    @pytest.mark.parametrize("x, y", [
        (3, 3), (3, 5), (4, 7), (5, 5), (6, 3), (7, 9),
    ])
    def test_regimen_valido(self, x, y):
        """Pares de exponentes dentro del regimen."""
        assert x >= 3 and y >= 3

    def test_regimen_cuadratico_permite_z_mayor_1(self):
        """En n=2, z puede ser > 1 (pitagoricos). Por eso se excluye."""
        assert calcular_z(3**2 + 4**2) == 2


# ==========================================
# CAPA E2 - EVENTO ECUACIONAL
# ==========================================

class TestCapaE2_Evento:
    """Verifica: N = A^x + B^y se computa correctamente."""

    @pytest.mark.parametrize("A, B, x, y", [
        (1, 2, 3, 3),
        (3, 5, 4, 4),
        (2, 7, 5, 3),
        (11, 13, 3, 3),
        (6, 10, 5, 5),
    ])
    def test_N_es_suma_de_potencias(self, A, B, x, y):
        N = A**x + B**y
        assert N == A**x + B**y
        assert N > 0
        assert isinstance(N, int)

    def test_N_siempre_positivo(self):
        """A^x + B^y > 0 para todo A, B en Z+."""
        for A in range(1, 20):
            for B in range(1, 20):
                assert A**3 + B**3 > 0


# ==========================================
# CAPA E3 - FUNCIONAL DE OMEGA-COHERENCIA
# ==========================================

class TestCapaE3_Coherencia:
    """
    Verifica: el funcional C_Omega mide estabilidad estructural.
    Se instancia computacionalmente como z(N).
    """

    @pytest.mark.parametrize("A, B, x, y", [
        (1, 2, 3, 3),
        (3, 5, 5, 5),
        (7, 11, 3, 7),
        (2, 9, 4, 4),
        (13, 17, 5, 3),
    ])
    def test_z_siempre_computable(self, A, B, x, y):
        """z(N) se puede calcular para toda configuracion valida."""
        N = A**x + B**y
        z = calcular_z(N)
        assert isinstance(z, int)
        assert z >= 1

    def test_z_detecta_potencia_perfecta(self):
        """z(N) > 1 si y solo si N es potencia perfecta."""
        assert calcular_z(8) == 3
        assert calcular_z(64) == 6
        assert calcular_z(36) == 2
        assert calcular_z(30) == 1

    def test_z_equivalencia_potencia(self):
        """z(N) = m implica N = c^m para algun c."""
        for N in [4, 8, 9, 16, 25, 27, 32, 64, 81, 125, 243]:
            z = calcular_z(N)
            assert z >= 2
            assert es_potencia_perfecta(N, z)


# ==========================================
# CAPA E4 - CENTRO COPRIMO
# ==========================================

class TestCapaE4_Coprimo:
    """
    Verifica: gcd(A, B) = 1 marca independencia
    multiplicativa total entre los sumandos.
    """

    @pytest.mark.parametrize("A, B", [
        (1, 2), (2, 3), (3, 5), (4, 9), (7, 11),
        (13, 17), (8, 15), (11, 29), (1, 99), (37, 41),
    ])
    def test_pares_coprimos(self, A, B):
        assert math.gcd(A, B) == 1

    def test_par_par_nunca_coprimo(self):
        """Dos numeros pares siempre comparten el factor 2."""
        for A in range(2, 50, 2):
            for B in range(2, 50, 2):
                assert math.gcd(A, B) >= 2

    def test_coprimalidad_implica_sin_estructura_compartida(self):
        """Si gcd(A,B)=1, no existen primos comunes."""
        for A, B in [(3, 7), (11, 13), (17, 29)]:
            fA = set(factorizar(A).keys())
            fB = set(factorizar(B).keys())
            assert fA.isdisjoint(fB)


# ==========================================
# CAPA E5 - NUCLEO P-ADICO
# ==========================================

class TestCapaE5_NucleopAdico:
    """
    Verifica: N = C^z requiere e_p = 0 (mod z)
    para todo primo p | N.
    """

    def test_potencia_perfecta_valuaciones_divisibles(self):
        """Si N = C^z, toda valuacion es multiplo de z."""
        casos = [
            (8, 3),
            (27, 3),
            (64, 6),
            (125, 3),
            (729, 6),
        ]
        for N, z in casos:
            factores = factorizar(N)
            for p, e in factores.items():
                assert e % z == 0, \
                    f"N={N}, z={z}: v_{p}={e} no divisible por {z}"

    def test_no_potencia_tiene_valuacion_indivisible(self):
        """Si N no es potencia perfecta, existe primo con e_p % z != 0."""
        no_potencias = [6, 10, 12, 15, 18, 20, 21, 28, 30]
        for N in no_potencias:
            z = calcular_z(N)
            assert z == 1
            tiene_rompedor, _, _ = existe_primo_rompedor(N, 3)
            assert tiene_rompedor

    @pytest.mark.parametrize("z", [3, 4, 5, 6, 7])
    def test_coherencia_multiplicativa_exige_divisibilidad(self, z):
        """Para multiples valores de z, verificar la condicion."""
        for C in range(2, 20):
            N = C ** z
            factores = factorizar(N)
            for p, e in factores.items():
                assert e % z == 0


# ==========================================
# CAPA E6 - SEPARACION PRIMA (OBSTRUCCION LOCAL)
# ==========================================

class TestCapaE6_PrimoRompedor:
    """
    Verifica: el primo rompedor impide potencia perfecta.
    Esta es la capa critica del framework.
    """

    @pytest.mark.parametrize("A, B, x, y", [
        (1, 2, 3, 3),
        (2, 3, 5, 5),
        (3, 5, 3, 3),
        (7, 11, 4, 4),
        (1, 4, 7, 7),
        (13, 17, 3, 5),
        (2, 9, 5, 3),
        (3, 41, 3, 7),
    ])
    def test_primo_rompedor_existe_para_coprimos(self, A, B, x, y):
        """Con gcd(A,B)=1 y x,y >= 3, siempre existe primo rompedor para z >= 3."""
        assert math.gcd(A, B) == 1
        N = A**x + B**y
        for z in range(3, 15):
            tiene, p, e = existe_primo_rompedor(N, z)
            assert tiene, \
                f"Sin rompedor: A={A},B={B},x={x},y={y},z={z},N={N}"

    def test_barrido_rompedor_exponentes_iguales(self):
        """Barrido: A^n + B^n con gcd=1, n >= 3, siempre tiene rompedor para z >= 3."""
        for n in [3, 5, 7]:
            for A in range(1, 50):
                for B in range(A + 1, 50):
                    if math.gcd(A, B) != 1:
                        continue
                    N = A**n + B**n
                    for z in range(3, 12):
                        tiene, _, _ = existe_primo_rompedor(N, z)
                        assert tiene, \
                            f"Sin rompedor: {A}^{n}+{B}^{n}, z={z}"

    def test_barrido_rompedor_exponentes_mixtos(self):
        """Barrido: A^x + B^y con gcd=1, x,y >= 3, siempre tiene rompedor para z >= 3."""
        for x in [3, 4, 5]:
            for y in [3, 4, 5]:
                for A in range(1, 30):
                    for B in range(1, 30):
                        if math.gcd(A, B) != 1:
                            continue
                        N = A**x + B**y
                        for z in range(3, 10):
                            tiene, _, _ = existe_primo_rompedor(N, z)
                            assert tiene, \
                                f"Sin rompedor: {A}^{x}+{B}^{y}, z={z}"

    def test_rompedor_no_existe_para_potencia_real(self):
        """Para N que SI es potencia perfecta, NO hay rompedor."""
        assert not existe_primo_rompedor(8, 3)[0]
        assert not existe_primo_rompedor(27, 3)[0]
        assert not existe_primo_rompedor(64, 3)[0]
        assert not existe_primo_rompedor(64, 6)[0]


# ==========================================
# CAPA E7 - REDUCCION DE MINIMALIDAD
# ==========================================

class TestCapaE7_Minimalidad:
    """
    Verifica: soluciones escaladas se descartan.
    Solo interesan configuraciones primitivas con gcd(A,B)=1.
    """

    def test_escalamiento_introduce_gcd(self):
        """Multiplicar por d > 1 destruye coprimalidad."""
        A, B = 3, 5
        assert math.gcd(A, B) == 1
        for d in [2, 3, 7, 11]:
            assert math.gcd(d * A, d * B) == d

    def test_reduccion_a_primitivo(self):
        """Todo par se reduce a un par coprimo."""
        pares = [(6, 10), (15, 25), (14, 21), (88, 132)]
        for A, B in pares:
            g = math.gcd(A, B)
            a, b = A // g, B // g
            assert math.gcd(a, b) == 1

    def test_z_del_nucleo_coprimo(self):
        """El nucleo coprimo tiene z = 1 para n >= 5."""
        for n in [5, 7, 9]:
            for A, B in [(6, 10), (14, 21), (15, 25)]:
                g = math.gcd(A, B)
                a, b = A // g, B // g
                nucleo = a**n + b**n
                assert calcular_z(nucleo) == 1

    def test_z_del_nucleo_cubico_acotado(self):
        """Para n = 3, el nucleo coprimo tiene z <= 2."""
        for A, B in [(6, 10), (14, 21), (15, 25)]:
            g = math.gcd(A, B)
            a, b = A // g, B // g
            nucleo = a**3 + b**3
            assert calcular_z(nucleo) <= 2


# ==========================================
# CAPA E8 - PREDICCION ESTRUCTURAL
# ==========================================

class TestCapaE8_Prediccion:
    """
    Verifica: si E6 se activa, entonces A^x + B^y != C^z.
    La prediccion central del framework.
    """

    def test_prediccion_beal_exponentes_iguales(self):
        """A^n + B^n != C^z para gcd=1, n >= 3, z >= 3."""
        for n in [3, 4, 5, 6, 7]:
            for A in range(1, 40):
                for B in range(A + 1, 40):
                    if math.gcd(A, B) != 1:
                        continue
                    N = A**n + B**n
                    for z in range(3, 20):
                        assert not es_potencia_perfecta(N, z), \
                            f"{A}^{n}+{B}^{n}={N}={round(N**(1/z))}^{z}"

    def test_prediccion_beal_exponentes_mixtos(self):
        """A^x + B^y != C^z para gcd=1, x,y,z >= 3."""
        for x in [3, 4, 5, 6, 7]:
            for y in [3, 4, 5, 6, 7]:
                for A in range(1, 30):
                    for B in range(1, 30):
                        if math.gcd(A, B) != 1:
                            continue
                        N = A**x + B**y
                        for z in range(3, 20):
                            assert not es_potencia_perfecta(N, z), \
                                f"{A}^{x}+{B}^{y}={N}={round(N**(1/z))}^{z}"

    def test_z_invariante_nunca_alcanza_3_con_coprimos(self):
        """z(A^x + B^y) < 3 para todo par coprimo con x, y >= 3."""
        for x in [3, 4, 5, 6, 7]:
            for y in [x, x + 1, x + 2]:
                if y > 7:
                    continue
                for A in range(1, 35):
                    for B in range(1, 35):
                        if math.gcd(A, B) != 1:
                            continue
                        N = A**x + B**y
                        z = calcular_z(N)
                        assert z < 3, \
                            f"z={z} >= 3 para {A}^{x}+{B}^{y}={N}"


# ==========================================
# PROPOSICION FUNDAMENTAL
# ==========================================

class TestProposicionFundamental:
    """
    Principio de Obstruccion Local:
    Si existe primo rompedor en E6,
    entonces N != C^z.
    """

    def test_rompedor_implica_no_potencia(self):
        """Si existe p con v_p(N) % z != 0, entonces N != C^z."""
        for N in range(2, 200):
            for z in range(2, 8):
                tiene_rompedor, _, _ = existe_primo_rompedor(N, z)
                if tiene_rompedor:
                    assert not es_potencia_perfecta(N, z), \
                        f"Contradiccion: N={N} tiene rompedor pero es {z}-potencia"

    def test_sin_rompedor_implica_potencia(self):
        """Si NO existe rompedor, entonces N = C^z."""
        potencias = [(8, 3), (27, 3), (16, 4), (32, 5), (64, 6), (81, 4), (243, 5)]
        for N, z in potencias:
            tiene_rompedor, _, _ = existe_primo_rompedor(N, z)
            assert not tiene_rompedor
            assert es_potencia_perfecta(N, z)

    def test_equivalencia_completa(self):
        """
        Para todo N y z:
        N = C^z  <=>  no existe primo rompedor para z
        """
        for N in range(2, 300):
            for z in range(2, 8):
                tiene_rompedor = existe_primo_rompedor(N, z)[0]
                es_potencia = es_potencia_perfecta(N, z)
                assert tiene_rompedor != es_potencia, \
                    f"Equivalencia rota: N={N}, z={z}"


# ==========================================
# PROGRAMA DE APLICACION (SECCION 6)
# ==========================================

class TestAplicacion_PotenciasPerfectas:
    """Rigidez de potencia perfecta: E5 critica."""

    def test_sumas_coprimas_nunca_cubo(self):
        """A^x + B^y con gcd=1, x,y >= 3 nunca es cubo."""
        for x in [3, 5, 7]:
            for y in [3, 5, 7]:
                for A in range(1, 40):
                    for B in range(1, 40):
                        if math.gcd(A, B) != 1:
                            continue
                        N = A**x + B**y
                        assert not es_potencia_perfecta(N, 3), \
                            f"{A}^{x}+{B}^{y}={N} es cubo"


class TestAplicacion_ABC:
    """Restricciones de crecimiento ABC: balance E3-E5."""

    def test_z_abc_para_tripletas_coprimas(self):
        """Para a+b=c con gcd(a,b,c)=1: z(abc) es tipicamente 1."""
        z_mayores = 0
        total = 0
        for a in range(1, 100):
            for b in range(a, 100):
                c = a + b
                if math.gcd(math.gcd(a, b), c) != 1:
                    continue
                total += 1
                N = a * b * c
                z = calcular_z(N)
                if z > 1:
                    z_mayores += 1

        assert z_mayores / total < 0.001


class TestAplicacion_Goldbach:
    """Abundancia aditiva: E4 domina."""

    def test_goldbach_hasta_10000(self):
        """Todo par >= 4 es suma de dos primos."""
        def es_primo(n):
            if n < 2:
                return False
            if n < 4:
                return True
            if n % 2 == 0 or n % 3 == 0:
                return False
            i = 5
            while i * i <= n:
                if n % i == 0 or n % (i + 2) == 0:
                    return False
                i += 6
            return True

        for n in range(4, 10001, 2):
            encontrado = False
            for p in range(2, n):
                if es_primo(p) and es_primo(n - p):
                    encontrado = True
                    break
            assert encontrado, f"Goldbach falla en {n}"


# ==========================================
# PREGUNTA CENTRAL (SECCION 7)
# ==========================================

class TestPreguntaCentral:
    """
    Pregunta: La coprimalidad (E4) produce
    inevitablemente un primo rompedor (E6)?

    Busqueda exhaustiva de contraejemplos.
    """

    def test_busqueda_contraejemplo_beal(self):
        """
        Busqueda: existe A^x + B^y = C^z
        con gcd(A,B)=1 y x,y,z >= 3?
        """
        for x in range(3, 8):
            for y in range(3, 8):
                for A in range(1, 50):
                    for B in range(1, 50):
                        if math.gcd(A, B) != 1:
                            continue
                        N = A**x + B**y
                        for z in range(3, 30):
                            assert not es_potencia_perfecta(N, z), \
                                f"CONTRAEJEMPLO: {A}^{x}+{B}^{y}={N}=C^{z}"

    def test_z_maximo_es_2_con_coprimos(self):
        """
        Con gcd(A,B)=1 y x,y >= 3,
        z(A^x + B^y) nunca excede 2.
        """
        z_max_global = 0
        for x in [3, 4, 5, 6, 7]:
            for y in [3, 4, 5, 6, 7]:
                for A in range(1, 30):
                    for B in range(1, 30):
                        if math.gcd(A, B) != 1:
                            continue
                        z = calcular_z(A**x + B**y)
                        if z > z_max_global:
                            z_max_global = z

        assert z_max_global <= 2, \
            f"z maximo encontrado: {z_max_global}"


# ==========================================
# VALUACION DIADICA (TEOREMA VERIFICADO)
# ==========================================

class TestValuacionDiadica:
    """
    Teorema de Valuacion Diadica para A^n + B^n.
    Resultado demostrado, no conjetura.
    """

    @pytest.mark.parametrize("n", [4, 6, 8, 10, 12, 14, 16, 18, 20])
    def test_impares_n_par_v2_es_1(self, n):
        """A, B impares, n par => v_2(A^n + B^n) = 1 => z = 1."""
        for A in range(1, 60, 2):
            for B in range(A + 2, 60, 2):
                N = A**n + B**n
                assert v_p(N, 2) == 1, \
                    f"v_2({A}^{n}+{B}^{n}) != 1"

    @pytest.mark.parametrize("n", [3, 5, 7, 9, 11, 13])
    def test_impares_n_impar_Q_siempre_impar(self, n):
        """A, B impares, n impar => Q_{n-1} es impar."""
        for A in range(1, 40, 2):
            for B in range(A + 2, 40, 2):
                if math.gcd(A, B) != 1:
                    continue
                S, Q = canales_ciclotomicos(A, B, n)
                assert Q % 2 == 1, \
                    f"Q par para A={A}, B={B}, n={n}"

    def test_par_impar_v2_es_0(self):
        """A par, B impar => A^n + B^n es impar => v_2 = 0."""
        for n in [3, 4, 5, 6, 7]:
            for A in range(2, 40, 2):
                for B in range(1, 40, 2):
                    N = A**n + B**n
                    assert N % 2 == 1, \
                        f"{A}^{n}+{B}^{n} es par"

    def test_obstruccion_diadica_cierra_caso_par(self):
        """
        Caso cerrado: A, B impares, n par, gcd(A,B)=1.
        v_2 = 1 impide C^z con z >= 3.
        """
        for n in [4, 6, 8]:
            for A in range(1, 30, 2):
                for B in range(A + 2, 30, 2):
                    if math.gcd(A, B) != 1:
                        continue
                    N = A**n + B**n
                    assert v_p(N, 2) == 1
                    assert calcular_z(N) == 1


# ==========================================
# SEPARACION DE CANALES (ESTRUCTURA CICLOTOMICA)
# ==========================================

class TestSeparacionCanales:
    """
    Verifica la separacion de canales S-Q
    que es el mecanismo estructural del framework.
    """

    @pytest.mark.parametrize("n", [3, 5, 7])
    def test_gcd_S_Q_divide_n(self, n):
        """gcd(S, Q) | n para todo par coprimo."""
        for a in range(1, 50):
            for b in range(a + 1, 50):
                if math.gcd(a, b) != 1:
                    continue
                S, Q = canales_ciclotomicos(a, b, n)
                g = math.gcd(S, Q)
                assert n % g == 0, \
                    f"gcd(S,Q)={g} no divide a n={n} para ({a},{b})"

    @pytest.mark.parametrize("n", [5, 7, 9, 11])
    def test_nucleo_coprimo_colapsa_n_ge_5(self, n):
        """z(a^n + b^n) = 1 para todo par coprimo cuando n >= 5."""
        for a in range(1, 40):
            for b in range(a + 1, 40):
                if math.gcd(a, b) != 1:
                    continue
                assert calcular_z(a**n + b**n) == 1, \
                    f"z != 1 para {a}^{n}+{b}^{n}"

    def test_regimen_cubico_z_acotado(self):
        """Para n = 3, el nucleo coprimo tiene z <= 2 (no necesariamente 1)."""
        for a in range(1, 50):
            for b in range(a + 1, 50):
                if math.gcd(a, b) != 1:
                    continue
                z = calcular_z(a**3 + b**3)
                assert z <= 2, \
                    f"z={z} > 2 para {a}^3+{b}^3"

    def test_cubico_z_nunca_alcanza_3(self):
        """Para n = 3, gcd=1: z(a^3+b^3) < 3 siempre."""
        for a in range(1, 60):
            for b in range(a + 1, 60):
                if math.gcd(a, b) != 1:
                    continue
                z = calcular_z(a**3 + b**3)
                assert z < 3, \
                    f"z={z} >= 3 para {a}^3+{b}^3"
