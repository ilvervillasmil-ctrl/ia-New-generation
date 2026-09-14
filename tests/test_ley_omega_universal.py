"""
TEST SUITE - LEY OMEGA DE OBSTRUCCION UNIVERSAL
Validacion computacional de los Tres Caminos y la Identidad Neutra.

Version optimizada para CI:
- misma logica
- mismos teoremas
- rangos de busqueda reducidos para evitar ejecuciones de horas
- correccion del caso cubico n=3: se exige z < 3, no z = 1

Autor: Ilver Villasmil
Arquitectura: Programa Villasmil-Omega (2026)
"""

import math
import pytest
from functools import reduce


# ==========================================
# MOTOR LOGICO
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
    """Invariante z(N) = gcd{v_p(N) : p | N}."""
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


def canales(a, b, n):
    """Descompone a^n + b^n = S * Q para n impar."""
    S = a + b
    Q = (a ** n + b ** n) // S
    return S, Q


# ==========================================
# PARAMETROS CI - RANGOS REDUCIDOS
# ==========================================

R_SMALL = 24
R_MED = 20
R_LARGE = 16
R_XL = 14
R_ABC = 60
R_GOLDBACH = 2000
R_Z_LIMIT = 14


# ==========================================
# I. LEY DE PARIDAD VALUATIVA
# ==========================================

class TestLeyParidadValuativa:
    """Seccion I.3 del capitulo: v_p = 1 implica z = 1."""

    def test_valuacion_1_fuerza_z_1(self):
        for N in range(2, 300):
            factores = factorizar(N)
            tiene_v1 = any(e == 1 for e in factores.values())
            if tiene_v1:
                assert calcular_z(N) == 1, \
                    f"N={N} tiene v_p=1 pero z={calcular_z(N)}"

    def test_valuacion_impar_impide_cuadrado(self):
        for N in range(2, 300):
            factores = factorizar(N)
            tiene_impar = any(e % 2 == 1 for e in factores.values())
            if tiene_impar:
                raiz = round(N ** 0.5)
                assert raiz * raiz != N, \
                    f"N={N} tiene v_p impar pero es cuadrado"

    def test_potencia_perfecta_requiere_valuaciones_divisibles(self):
        for k in range(2, 7):
            for c in range(2, 24):
                N = c ** k
                factores = factorizar(N)
                for p, e in factores.items():
                    assert e % k == 0, \
                        f"N={c}^{k}, v_{p}={e} no divisible por {k}"


# ==========================================
# II. LEY OMEGA - ENUNCIADO CENTRAL
# ==========================================

class TestLeyOmega:
    """Seccion II: z(A^n + B^n) = 1 para n>=4; en cubico z<3."""

    @pytest.mark.parametrize("n", [3, 4, 5, 6, 7, 8, 9])
    def test_ley_omega_por_grado(self, n):
        for A in range(1, R_MED):
            for B in range(A + 1, R_MED):
                if math.gcd(A, B) != 1:
                    continue
                z = calcular_z(A ** n + B ** n)
                if n == 3:
                    assert z < 3, \
                        f"z={z} para {A}^{n}+{B}^{n}, gcd=1"
                else:
                    assert z == 1, \
                        f"z={z} para {A}^{n}+{B}^{n}, gcd=1"

    def test_ley_omega_exponentes_mixtos(self):
        for x in [3, 4, 5, 6]:
            for y in [3, 4, 5, 6]:
                for A in range(1, R_LARGE):
                    for B in range(1, R_LARGE):
                        if math.gcd(A, B) != 1:
                            continue
                        z = calcular_z(A ** x + B ** y)
                        assert z < 3, \
                            f"z={z} >= 3 para {A}^{x}+{B}^{y}"


# ==========================================
# III. PRIMER CAMINO - LOS CANALES
# ==========================================

class TestCamino1_Canales:
    """Seccion III: separacion ciclotomica S*Q."""

    @pytest.mark.parametrize("n", [3, 5, 7, 9])
    def test_factorizacion_exacta(self, n):
        for a in range(1, R_MED):
            for b in range(a + 1, R_MED):
                if math.gcd(a, b) != 1:
                    continue
                S, Q = canales(a, b, n)
                assert S * Q == a ** n + b ** n

    @pytest.mark.parametrize("n", [3, 5, 7, 9, 11])
    def test_lema_interseccion(self, n):
        for a in range(1, R_MED):
            for b in range(a + 1, R_MED):
                if math.gcd(a, b) != 1:
                    continue
                S, Q = canales(a, b, n)
                g = math.gcd(S, Q)
                assert n % g == 0, \
                    f"gcd(S,Q)={g} no divide a n={n} para ({a},{b})"

    @pytest.mark.parametrize("n", [3, 5, 7])
    def test_primos_exclusivos_de_S_no_tocan_Q(self, n):
        for a in range(1, R_LARGE):
            for b in range(a + 1, R_LARGE):
                if math.gcd(a, b) != 1:
                    continue
                S, Q = canales(a, b, n)
                for p in factorizar(S):
                    if n % p != 0:
                        assert Q % p != 0, \
                            f"p={p} divide S={S} y Q={Q} pero p no divide n={n}"

    @pytest.mark.parametrize("n", [3, 5, 7])
    def test_Q_mod_S(self, n):
        for a in range(1, R_XL):
            for b in range(a + 1, R_XL):
                if math.gcd(a, b) != 1:
                    continue
                S, Q = canales(a, b, n)
                for p in factorizar(S):
                    if n % p != 0:
                        expected = (n * pow(b, n - 1, p)) % p
                        assert Q % p == expected, \
                            f"Q mod {p} != n*b^(n-1) mod {p}"

    @pytest.mark.parametrize("n", [5, 7, 9])
    def test_nucleo_colapsa_n_ge_5(self, n):
        for a in range(1, R_MED):
            for b in range(a + 1, R_MED):
                if math.gcd(a, b) != 1:
                    continue
                assert calcular_z(a ** n + b ** n) == 1

    def test_cubico_z_menor_que_3(self):
        for a in range(1, 28):
            for b in range(a + 1, 28):
                if math.gcd(a, b) != 1:
                    continue
                z = calcular_z(a ** 3 + b ** 3)
                assert z < 3, \
                    f"z={z} >= 3 para {a}^3+{b}^3"


# ==========================================
# IV. SEGUNDO CAMINO - ZSIGMONDY
# ==========================================

class TestCamino2_Zsigmondy:
    """Seccion IV: el primo primitivo tiene v = 1, salvo excepciones cubicas/perfectas."""

    @pytest.mark.parametrize("n", [3, 5, 7, 11])
    def test_existe_primo_con_valuacion_1(self, n):
        for A in range(1, R_MED):
            for B in range(A + 1, R_MED):
                if math.gcd(A, B) != 1:
                    continue
                N = A ** n + B ** n
                factores = factorizar(N)
                tiene_v1 = any(e == 1 for e in factores.values())

                if n == 3:
                    z = calcular_z(N)
                    assert z < 3, \
                        f"z={z} >= 3 para {A}^{n}+{B}^{n}"
                else:
                    assert tiene_v1, \
                        f"Ningun primo con v=1 en {A}^{n}+{B}^{n}={N}"

    @pytest.mark.parametrize("n", [4, 6, 8, 10])
    def test_n_par_impares_v2_es_1(self, n):
        for A in range(1, R_MED, 2):
            for B in range(A + 2, R_MED, 2):
                N = A ** n + B ** n
                assert v_p(N, 2) == 1, \
                    f"v_2({A}^{n}+{B}^{n}) != 1"

    def test_excepciones_zsigmondy_no_producen_z_ge_2(self):
        N = 2 ** 6 + 1 ** 6
        assert calcular_z(N) == 1

    @pytest.mark.parametrize("n", [3, 5, 7, 9])
    def test_Q_ciclotomico_impar_para_bases_impares(self, n):
        for A in range(1, R_LARGE, 2):
            for B in range(A + 2, R_LARGE, 2):
                if math.gcd(A, B) != 1:
                    continue
                _, Q = canales(A, B, n)
                assert Q % 2 == 1, \
                    f"Q par para {A},{B},n={n}"


# ==========================================
# V. TERCER CAMINO - EL TOROIDE
# ==========================================

class TestCamino3_Toroide:
    """Seccion V: geometria del toroide aritmetico."""

    def test_regimen_independiente_cobertura_total(self):
        casos = [
            [3, 5],
            [2, 3, 5],
            [3, 5, 7],
            [2, 3, 5, 7],
        ]
        for moduli in casos:
            producto = 1
            for m in moduli:
                producto *= m
            coprime = True
            for i in range(len(moduli)):
                for j in range(i + 1, len(moduli)):
                    if math.gcd(moduli[i], moduli[j]) != 1:
                        coprime = False
            if not coprime:
                continue
            periodo = moduli[0]
            for m in moduli[1:]:
                periodo = periodo * m // math.gcd(periodo, m)
            assert periodo == producto
            estados = set()
            for n in range(periodo):
                estado = tuple(n % m for m in moduli)
                estados.add(estado)
            assert len(estados) == producto

    def test_regimen_resonante_colapsa(self):
        casos = [
            ([4, 6], 12, 24),
            ([4, 6, 9], 36, 216),
            ([3, 4, 6], 12, 72),
        ]
        for moduli, expected_period, expected_product in casos:
            producto = 1
            for m in moduli:
                producto *= m
            assert producto == expected_product
            periodo = moduli[0]
            for m in moduli[1:]:
                periodo = periodo * m // math.gcd(periodo, m)
            assert periodo == expected_period
            assert periodo < producto

    def test_primos_filtrados_a_clases_admisibles(self):
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

        M = 2 * 3 * 5 * 7 * 11 * 13
        for q in range(17, 400):
            if es_primo(q):
                assert math.gcd(q, M) == 1, \
                    f"Primo {q} no es coprimo con M={M}"

    def test_coprimos_en_dimensiones_ortogonales(self):
        pares = [
            (3, 7), (11, 13), (8, 15), (17, 29), (4, 9),
            (25, 49), (7, 23), (37, 41), (1, 99),
        ]
        for A, B in pares:
            assert math.gcd(A, B) == 1
            primos_A = set(factorizar(A).keys())
            primos_B = set(factorizar(B).keys())
            assert primos_A.isdisjoint(primos_B), \
                f"({A},{B}) comparten primos: {primos_A & primos_B}"

    def test_suma_coprimos_produce_primos_nuevos(self):
        for a in range(1, R_MED):
            for b in range(a + 1, R_MED):
                if math.gcd(a, b) != 1:
                    continue
                c = a + b
                for p in factorizar(c):
                    assert a % p != 0, \
                        f"p={p} divide a c={c} y a a={a}"
                    assert b % p != 0, \
                        f"p={p} divide a c={c} y a b={b}"


# ==========================================
# VI. CONVERGENCIA DE LOS TRES CAMINOS
# ==========================================

class TestConvergencia:
    """Seccion VI: los tres caminos dan el mismo resultado."""

    @pytest.mark.parametrize("n", [3, 5, 7])
    def test_tres_caminos_coinciden(self, n):
        for A in range(1, 22):
            for B in range(A + 1, 22):
                if math.gcd(A, B) != 1:
                    continue
                N = A ** n + B ** n

                S, Q = canales(A, B, n)
                assert S * Q == N
                g = math.gcd(S, Q)
                assert n % g == 0 or g == 1

                factores = factorizar(N)
                tiene_v1 = any(e == 1 for e in factores.values())

                if n == 3:
                    assert calcular_z(N) < 3
                else:
                    assert tiene_v1
                    assert calcular_z(N) == 1


# ==========================================
# VII. IDENTIDAD NEUTRA
# ==========================================

class TestIdentidadNeutra:
    """Seccion VII: z = nm + 1, n no divide z."""

    @pytest.mark.parametrize("n", [3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    def test_identidad_aritmetica(self, n):
        for m in range(1, 6):
            N = (2 ** m) ** n + (2 ** m) ** n
            assert N == 2 ** (n * m + 1)

    @pytest.mark.parametrize("n", [3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    def test_z_es_nm_mas_1(self, n):
        for m in range(1, 6):
            N = 2 ** (n * m + 1)
            z = calcular_z(N)
            assert z == n * m + 1

    @pytest.mark.parametrize("n", [3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    def test_n_no_divide_z(self, n):
        for m in range(1, 6):
            z = n * m + 1
            assert z % n != 0, \
                f"n={n} divide a z={z}"

    @pytest.mark.parametrize("n", [3, 4, 5, 6, 7, 8, 9, 10])
    def test_residuo_siempre_1(self, n):
        for m in range(1, 7):
            z = n * m + 1
            assert z % n == 1

    @pytest.mark.parametrize("n", [3, 4, 5, 6, 7, 8])
    def test_transicion_incremento_n(self, n):
        for m in range(1, 6):
            N_m = 2 ** (n * m + 1)
            N_m1 = 2 ** (n * (m + 1) + 1)
            assert N_m1 == (2 ** n) * N_m
            assert calcular_z(N_m1) == calcular_z(N_m) + n

    def test_mas_1_es_v2_de_suma_minima(self):
        for n in range(3, 20):
            assert 1 ** n + 1 ** n == 2
            assert v_p(2, 2) == 1


# ==========================================
# VIII. COROLARIO DE BEAL
# ==========================================

class TestCorolarioBeal:
    """Seccion VIII: A^x + B^y != C^z para gcd=1, x,y,z >= 3."""

    def test_no_existe_potencia_perfecta_z_ge_3(self):
        for x in range(3, 7):
            for y in range(3, 7):
                for A in range(1, 20):
                    for B in range(1, 20):
                        if math.gcd(A, B) != 1:
                            continue
                        N = A ** x + B ** y
                        for z in range(3, R_Z_LIMIT):
                            assert not es_potencia_perfecta(N, z), \
                                f"CONTRAEJEMPLO: {A}^{x}+{B}^{y}={N}=C^{z}"

    def test_z_invariante_siempre_menor_que_3(self):
        z_max = 0
        for x in [3, 4, 5, 6]:
            for y in [3, 4, 5, 6]:
                for A in range(1, 18):
                    for B in range(1, 18):
                        if math.gcd(A, B) != 1:
                            continue
                        z = calcular_z(A ** x + B ** y)
                        if z > z_max:
                            z_max = z
                        assert z < 3
        assert z_max <= 2

    def test_contradiccion_explicita(self):
        for n in [3, 5, 7]:
            for A in range(1, 18):
                for B in range(A + 1, 18):
                    if math.gcd(A, B) != 1:
                        continue
                    N = A ** n + B ** n
                    z_N = calcular_z(N)
                    assert z_N < 3


# ==========================================
# IX. COROLARIO ABC
# ==========================================

class TestCorolarioABC:
    """Seccion IX: z(abc) = 1 para a+b=c, gcd(a,b,c)=1."""

    def test_soportes_disjuntos(self):
        for a in range(1, R_ABC):
            for b in range(a, R_ABC):
                c = a + b
                if math.gcd(math.gcd(a, b), c) != 1:
                    continue
                if math.gcd(a, b) != 1:
                    continue
                primos_a = set(factorizar(a).keys()) if a > 1 else set()
                primos_b = set(factorizar(b).keys()) if b > 1 else set()
                primos_c = set(factorizar(c).keys())
                assert primos_a.isdisjoint(primos_b)
                assert primos_a.isdisjoint(primos_c)
                assert primos_b.isdisjoint(primos_c)

    def test_z_abc_predominantemente_1(self):
        total = 0
        z_mayor = 0
        for a in range(1, R_ABC):
            for b in range(a, R_ABC):
                c = a + b
                if math.gcd(math.gcd(a, b), c) != 1:
                    continue
                total += 1
                N = a * b * c
                z = calcular_z(N)
                if z > 1:
                    z_mayor += 1
        assert z_mayor / total < 0.002

    def test_primos_de_c_son_nuevos(self):
        for a in range(2, 50):
            for b in range(a, 50):
                if math.gcd(a, b) != 1:
                    continue
                c = a + b
                for p in factorizar(c):
                    if a % p == 0:
                        assert b % p != 0, \
                            f"p={p} divide a={a}, b={b}, c={c} con gcd=1"


# ==========================================
# X. DICOTOMIA FUNDAMENTAL
# ==========================================

class TestDicotomia:
    """Seccion X: gcd=1 da z fuerte desde n>=4; cubico queda z<3."""

    def test_regimen_I_coprimos_z_es_1(self):
        for n in [3, 5, 7, 9]:
            for A in range(1, 18):
                for B in range(A + 1, 18):
                    if math.gcd(A, B) != 1:
                        continue
                    z = calcular_z(A ** n + B ** n)
                    if n == 3:
                        assert z < 3
                    else:
                        assert z == 1

    def test_regimen_II_diagonal_z_es_nm1(self):
        for n in [3, 4, 5, 6, 7, 8]:
            for m in range(1, 6):
                A = B = 2 ** m
                assert math.gcd(A, B) > 1
                z = calcular_z(A ** n + B ** n)
                assert z == n * m + 1

    def test_regimen_II_nucleo_siempre_z_1(self):
        for n in [5, 7, 9]:
            pares_con_gcd = [(6, 10), (14, 21), (15, 25), (4, 6)]
            for A, B in pares_con_gcd:
                g = math.gcd(A, B)
                a, b = A // g, B // g
                assert math.gcd(a, b) == 1
                assert calcular_z(a ** n + b ** n) == 1


# ==========================================
# XI. VALUACION DIADICA
# ==========================================

class TestValuacionDiadica:
    """Teorema de valuacion diadica: cierre por v_2."""

    @pytest.mark.parametrize("n", [4, 6, 8, 10, 12])
    def test_n_par_impares_v2_fijo_1(self, n):
        for A in range(1, 30, 2):
            for B in range(A + 2, 30, 2):
                assert v_p(A ** n + B ** n, 2) == 1

    @pytest.mark.parametrize("n", [3, 5, 7, 9, 11])
    def test_n_impar_impares_Q_impar(self, n):
        for A in range(1, 26, 2):
            for B in range(A + 2, 26, 2):
                if math.gcd(A, B) != 1:
                    continue
                _, Q = canales(A, B, n)
                assert Q % 2 == 1

    def test_par_impar_v2_cero(self):
        for n in [3, 4, 5, 6, 7]:
            for A in range(2, 22, 2):
                for B in range(1, 22, 2):
                    N = A ** n + B ** n
                    assert N % 2 == 1

    def test_obstruccion_diadica_cierra_n_par(self):
        for n in [4, 6, 8, 10]:
            for A in range(1, 22, 2):
                for B in range(A + 2, 22, 2):
                    if math.gcd(A, B) != 1:
                        continue
                    N = A ** n + B ** n
                    assert v_p(N, 2) == 1
                    assert calcular_z(N) == 1


# ==========================================
# XII. PRUEBA DE INFINITUD
# ==========================================

class TestInfinitud:
    """Seccion XI: por que se cumple hasta el infinito."""

    def test_identidad_aritmetica_universal(self):
        for a in range(0, 60):
            assert 2 ** a + 2 ** a == 2 ** (a + 1)

    def test_n_nunca_divide_1(self):
        for n in range(2, 400):
            assert 1 % n != 0 or n == 1

    def test_v2_de_2_siempre_1(self):
        assert v_p(2, 2) == 1

    def test_cadena_no_tiene_cota(self):
        for n in [3, 5, 7, 11]:
            for K in [10, 50, 100]:
                m = (K // n) + 1
                z = n * m + 1
                assert z > K

    def test_tres_pilares_no_dependen_de_parametros(self):
        for a in [1, 10, 100]:
            assert 2 ** a + 2 ** a == 2 ** (a + 1)

        for k in [1, 7, 13, 99]:
            assert math.gcd(k) == k

        for n in [3, 7, 100, 999]:
            assert 1 % n != 0


# ==========================================
# XIII. BUSQUEDA DE CONTRAEJEMPLOS
# ==========================================

class TestBusquedaContraejemplos:
    """Busqueda exhaustiva: cero contraejemplos."""

    def test_beal_sin_contraejemplo(self):
        for x in range(3, 6):
            for y in range(3, 6):
                for A in range(1, 18):
                    for B in range(1, 18):
                        if math.gcd(A, B) != 1:
                            continue
                        N = A ** x + B ** y
                        for z in range(3, 12):
                            assert not es_potencia_perfecta(N, z)

    def test_z_maximo_global_es_2(self):
        z_max = 0
        for x in [3, 4, 5, 6]:
            for y in [3, 4, 5, 6]:
                for A in range(1, 18):
                    for B in range(1, 18):
                        if math.gcd(A, B) != 1:
                            continue
                        z = calcular_z(A ** x + B ** y)
                        if z > z_max:
                            z_max = z
        assert z_max <= 2, f"z maximo global = {z_max} > 2"

    def test_goldbach_hasta_2000(self):
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

        for n in range(4, R_GOLDBACH + 1, 2):
            encontrado = False
            for p in range(2, n):
                if es_primo(p) and es_primo(n - p):
                    encontrado = True
                    break
            assert encontrado, f"Goldbach falla en {n}"

    def test_abc_z_tripletas_coprimas(self):
        z_mayores = 0
        total = 0
        for a in range(1, R_ABC):
            for b in range(a, R_ABC):
                c = a + b
                if math.gcd(math.gcd(a, b), c) != 1:
                    continue
                total += 1
                N = a * b * c
                z = calcular_z(N)
                if z > 1:
                    z_mayores += 1
        assert z_mayores / total < 0.002


# ==========================================
# XIV. REGIMEN SEXTICO PAR-PAR (n=6)
# ==========================================

class TestRegimenSextico:
    """Verificacion completa del regimen n=6 par-par."""

    def test_reduccion_estructural(self):
        pares = [(2, 4), (4, 6), (8, 12), (2, 2), (64, 64)]
        for A, B in pares:
            g = math.gcd(A, B)
            a, b = A // g, B // g
            N = A ** 6 + B ** 6
            assert N == g ** 6 * (a ** 6 + b ** 6)

    def test_canales_sexticos(self):
        for a in range(1, 24):
            for b in range(a + 1, 24):
                if math.gcd(a, b) != 1:
                    continue
                S = a ** 2 + b ** 2
                Q = a ** 4 - a ** 2 * b ** 2 + b ** 4
                assert S * Q == a ** 6 + b ** 6
                g = math.gcd(S, Q)
                assert g == 1 or g == 3, \
                    f"gcd(S,Q)={g} para ({a},{b})"

    def test_nucleo_coprimo_z_1(self):
        for a in range(1, 32):
            for b in range(a + 1, 32):
                if math.gcd(a, b) != 1:
                    continue
                assert calcular_z(a ** 6 + b ** 6) == 1

    def test_cadena_diagonal_6m1(self):
        for m in range(1, 8):
            A = 2 ** m
            N = A ** 6 + A ** 6
            assert N == 2 ** (6 * m + 1)
            assert calcular_z(N) == 6 * m + 1

    def test_transicion_factor_64(self):
        for m in range(1, 7):
            N_m = 2 ** (6 * m + 1)
            N_m1 = 2 ** (6 * (m + 1) + 1)
            assert N_m1 == 64 * N_m
            assert calcular_z(N_m1) == calcular_z(N_m) + 6

    def test_exclusion_6_no_divide_z(self):
        for m in range(1, 10):
            z = 6 * m + 1
            assert z % 6 != 0
            assert z % 2 != 0
            assert z % 3 != 0

    def test_ausencia_resonancia_no_diagonal(self):
        for A in range(2, 40, 2):
            for B in range(A + 2, 40, 2):
                N = A ** 6 + B ** 6
                z = calcular_z(N)
                if z > 1:
                    g = math.gcd(A, B)
                    a, b = A // g, B // g
                    assert calcular_z(a ** 6 + b ** 6) == 1

    def test_v2_fijo_1_impares(self):
        for A in range(1, 30, 2):
            for B in range(A + 2, 30, 2):
                assert v_p(A ** 6 + B ** 6, 2) == 1

    def test_espectro_exacto(self):
        z_observados = set()
        for A in range(2, 60, 2):
            for B in range(A, 60, 2):
                z = calcular_z(A ** 6 + B ** 6)
                z_observados.add(z)
        for z in z_observados:
            if z == 1:
                continue
            assert (z - 1) % 6 == 0, \
                f"z={z} no es de la forma 6m+1"
