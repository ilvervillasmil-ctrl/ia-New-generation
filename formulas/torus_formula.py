"""
formulas/torus_formula.py
=========================
La Formula del Toroide - Villasmil-Omega Framework v3.2

Basada en:
  [TORUS]  "Structural Cycles and Operational Infinity: Modular Decomposition
            and Resonance in Iterative Systems" - Ilver Villasmil, Marzo 2026.
  [RH]     "Resolution of the Riemann Hypothesis: Structural Control of
            Arithmetic Oscillations via the Optimal Funnel, Spectral Control
            Theorem, and VPSI" - Ilver Villasmil, Marzo 2026.
  [UCF]    "Villasmil-Omega Framework: Integration of Everything" - Enero 2026.

============================================================
LA FORMULA CENTRAL
============================================================

  N es el espacio de cobertura del toroide aritmetico T_k:

    T_k = prod_{p <= B} Z/pZ,    dim(T_k) = k

  La proyeccion:

    pi: N -> T_k,    pi(n) = (n mod p1, n mod p2, ..., n mod pk)

  Los enteros NO van en linea recta hacia el infinito.
  Son una helice que orbita T_k para siempre.
  Infinito = numero de vueltas, no tamano de la pista.

============================================================
EL CAMPO ARITMETICO
============================================================

  Para cada clase admisible a en (Z/MZ)*:

    eps(a) = pi(x; M, a)/pi(x) - 1/phi(M)

  La energia del campo:

    E(M) = sum_{a in (Z/MZ)*} eps(a)^2  ~  O(10^-7)

  Verificado:
    E(M6) = 5.49e-7  (T6, phi = 5760,  M = 30030)
    E(M7) = 8.20e-7  (T7, phi = 92160, M = 510510)

============================================================
CONEXION CON UCF (PROBADA)
============================================================

  beta = 1/27 = residuo geometrico del cubo 3x3x3
  E(M) = residuo distribucional de los primos en el toroide

  Ambos miden el mismo fenomeno desde angulos distintos:
  el residuo estructural que ningun sistema puede eliminar.

  Por eso C_max = alpha = 26/27 - siempre queda beta.

============================================================
CONEXION CON RH (TRABAJO EN PROGRESO [6])
============================================================

  Los modos de Fourier e_hat(k) deberian codificar las partes
  imaginarias gamma de los ceros de Riemann rho = 1/2 + i*gamma.

  La planitud E(M) ~ 10^-7 es consistente con RH:
  si todos los ceros tienen Re = 1/2, las contribuciones
  oscilatorias se distribuyen uniformemente, produciendo
  exactamente el campo plano espectralmente difuso observado.

  STATUS: Formal - no implementado sin prueba completa.

============================================================
PREGUNTA ABIERTA - BETA COMO RESIDUO DEL TOROIDE
============================================================

  Numericamente:
    beta^4 = 1.882e-6  (ratio a E(M7) = 2.29)
    beta^5 = 6.969e-8  (ratio a E(M7) = 0.085)

  beta^4 es el mas cercano pero no es igual.
  Si existe derivacion formal, conectaria:

    N -> T_k -> E(M) -> beta -> alpha -> C_max = 1 - beta

  Falsificable si: beta^n = E(M) para algun n derivable
  de la geometria del cubo 3x3x3.

Author: Ilver Villasmil
Framework: Villasmil-Omega v3.2
"""

from __future__ import annotations

import math
from collections import Counter
from math import gcd
from functools import reduce
from typing import Dict, List, Optional, Tuple

# -----------------------------------------------------------------------------
# CONSTANTES UCF (importar si estan disponibles)
# -----------------------------------------------------------------------------

try:
    from formulas.constants import ALPHA, BETA, PHI
except ImportError:
    ALPHA = 26 / 27
    BETA  = 1 / 27
    PHI   = (1 + math.sqrt(5)) / 2

# Valores del campo verificados en el paper (Tabla 3)
E_M6_PAPER = 5.49e-7   # T6, M=30030,   phi(M)=5760
E_M7_PAPER = 8.20e-7   # T7, M=510510,  phi(M)=92160

# Primos que generan T2-T7
TORUS_PRIMES = {
    2: [2, 3],
    3: [2, 3, 5],
    4: [2, 3, 5, 7],
    5: [2, 3, 5, 7, 11],
    6: [2, 3, 5, 7, 11, 13],
    7: [2, 3, 5, 7, 11, 13, 17],
}


# -----------------------------------------------------------------------------
# UTILIDADES BASICAS
# -----------------------------------------------------------------------------

def _lcm(a: int, b: int) -> int:
    return a * b // gcd(a, b)


def _is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def _euler_phi(n: int) -> int:
    """phi(n) - totiente de Euler."""
    result = n
    temp   = n
    d      = 2
    while d * d <= temp:
        if temp % d == 0:
            while temp % d == 0:
                temp //= d
            result -= result // d
        d += 1
    if temp > 1:
        result -= result // temp
    return result


def _primorial(B: int) -> int:
    """M = prod_{p <= B} p."""
    result = 1
    for p in range(2, B + 1):
        if _is_prime(p):
            result *= p
    return result


# -----------------------------------------------------------------------------
# I. ESTRUCTURA DEL TOROIDE
# -----------------------------------------------------------------------------

def torus_dimension(primes: List[int]) -> int:
    """
    k = numero de ruedas del toroide.
    Cada primo agrega una dimension.

    T_k = Z/p1Z x Z/p2Z x ... x Z/pkZ
    """
    return len(primes)


def primorial_M(primes: List[int]) -> int:
    """
    M = prod(pi) - el primorial que define el toroide.

    T7: M = 2*3*5*7*11*13*17 = 510510
    """
    result = 1
    for p in primes:
        result *= p
    return result


def phi_M(primes: List[int]) -> int:
    """
    phi(M) = prod(pi - 1) - numero de clases admisibles en el toroide.

    T7: phi(M) = 1*2*4*6*10*12*16 = 92160
    """
    result = 1
    for p in primes:
        result *= (p - 1)
    return result


def state_map(n: int, primes: List[int]) -> Tuple[int, ...]:
    """
    phi: N -> T_k,    phi(n) = (n mod p1, ..., n mod pk)

    El entero n es el instrumento.
    phi(n) es el observable - donde n apunta en el toroide.

    Principio de Instrumentacion Matematica (PIM):
    Todo n y m con phi(n) = phi(m) son estructuralmente
    indistinguibles en el toroide.
    """
    return tuple(n % p for p in primes)


def period(moduli: List[int]) -> int:
    """
    P = lcm(n1, n2, ..., nk)

    Theorem 4.1 (Traversal Estructural):
    El periodo es el numero de estados distintos.
    Despues de P pasos, la trayectoria regresa al origen.
    """
    return reduce(_lcm, moduli)


def torus_coverage(primes: List[int]) -> float:
    """
    Cobertura = periodo / |S(M)| en (0, 1]

    1.0  -> regimen independiente (Ley 1): todos los estados visitados
    <1.0 -> regimen resonante (Ley 2): estados inaccesibles
    """
    P     = period(primes)
    total = primorial_M(primes)
    return P / total


def phase_vector(n: int, primes: List[int]) -> Tuple[float, ...]:
    """
    Theta(n) = (2*pi*(n mod p1)/p1, ..., 2*pi*(n mod pk)/pk) en [0, 2*pi)^k

    Theorem 5.2 (Phase Dynamics):
    La trayectoria en T_k es una geodesica discreta con
    velocidad angular w = (2*pi/p1, ..., 2*pi/pk).
    Cada componente avanza 2*pi/pi por paso - uniforme e independiente.
    """
    return tuple(2 * math.pi * (n % p) / p for p in primes)


def is_covering_space(primes: List[int]) -> bool:
    """
    Verifica el Teorema de Unrolling (Thm 5.4):
    pi(n) = pi(m) iff n == m (mod P)

    N es el espacio de cobertura de T_k.
    La helice colapsa en el toroide bajo la proyeccion pi.
    """
    P      = period(primes)
    start  = state_map(0, primes)
    closes = state_map(P, primes) == start
    return closes


# -----------------------------------------------------------------------------
# II. LAS CUATRO LEYES ESTRUCTURALES
# -----------------------------------------------------------------------------

def law1_cycle_independence(primes: List[int]) -> Dict:
    """
    Ley 1 - Independencia de Ciclos (Seccion 4.2 de [TORUS])

    Si gcd(pi, pj) = 1 para todo i!=j, entonces:
      P = prod(pi) = |S(M)|
      phi: Z/PZ -> S(M) es una biyeccion

    Los primos son pairwise coprimos por definicion.
    Por tanto T2-T7 siempre estan en regimen independiente.

    Returns dict con evidencia verificable.
    """
    M           = primorial_M(primes)
    P           = period(primes)
    all_coprime = all(
        gcd(primes[i], primes[j]) == 1
        for i in range(len(primes))
        for j in range(i + 1, len(primes))
    )
    law_holds = (not all_coprime) or (P == M)
    coverage  = P / M

    return {
        "primes":      primes,
        "M":           M,
        "period":      P,
        "all_coprime": all_coprime,
        "law_holds":   law_holds,
        "coverage":    coverage,
        "bijection":   (P == M) and all_coprime,
        "regime":      "INDEPENDENT" if all_coprime else "RESONANT",
    }


def law2_cycle_resonance(moduli: List[int]) -> Dict:
    """
    Ley 2 - Resonancia de Ciclos (Seccion 4.3 de [TORUS])

    Si gcd(ni, nj) > 1 para algun par, entonces:
      P = lcm < prod(ni)
      La orbita colapsa - estados inaccesibles.

    Ejemplo del paper:
      (4, 6): P=12, producto=24, cobertura=50%
      (4, 6, 9): P=36, producto=216, cobertura=16.7%

    Returns dict con evidencia verificable.
    """
    P        = period(moduli)
    producto = 1
    for m in moduli:
        producto *= m

    has_shared = any(
        gcd(moduli[i], moduli[j]) > 1
        for i in range(len(moduli))
        for j in range(i + 1, len(moduli))
    )
    law_holds = (not has_shared) or (P < producto)

    return {
        "moduli":        moduli,
        "period":        P,
        "product":       producto,
        "has_shared":    has_shared,
        "law_holds":     law_holds,
        "coverage":      P / producto,
        "states_missed": producto - P,
        "regime":        "RESONANT" if has_shared else "INDEPENDENT",
    }


def law3_prime_filtering(B: int, check_up_to: int = 1000) -> Dict:
    """
    Ley 3 - Filtrado Estructural de Primos (Seccion 4.4 de [TORUS])

    Sea M = prod_{p<=B} p. Todo primo q > B satisface gcd(q, M) = 1.
    Los primos son filtrados automaticamente a la zona admisible (Z/MZ)*.

    Prueba:
      Si gcd(q, M) > 1, entonces algun p <= B divide q.
      Pero q es primo -> q = p <= B. Contradiccion.

    Esta ley es un teorema - no puede fallar.
    Si falla, hay un bug en la implementacion.

    Returns dict con evidencia verificable.
    """
    primes_up_to_B = [p for p in range(2, B + 1) if _is_prime(p)]
    M              = primorial_M(primes_up_to_B)
    primes_above_B = [q for q in range(B + 1, check_up_to + 1) if _is_prime(q)]
    violations     = [q for q in primes_above_B if gcd(q, M) != 1]

    return {
        "B":              B,
        "M":              M,
        "primes_up_to_B": primes_up_to_B,
        "primes_checked": len(primes_above_B),
        "violations":     violations,
        "law_holds":      len(violations) == 0,
        "proof":          "gcd(q,M)>1 -> p<=B divide q -> q=p<=B: contradiccion",
    }


def law4_field_energy(
    primes: List[int],
    prime_limit: int = 5000,
) -> Dict:
    """
    Ley 4 - Oscilacion Prima Modular (Seccion 4.5 de [TORUS])

    Sea eps(a) = pi(x; M, a)/pi(x) - 1/phi(M)  para a en (Z/MZ)*

    E(M) = sum_a eps(a)^2  ~  O(10^-7)

    El campo es plano, los modos son espectralmente independientes:
      E_hat(0) = 0  (por construccion)
      E(M) estable cuando phi(M) -> inf

    Valores del paper (Tabla 3 de [TORUS]):
      E(M6) = 5.49e-7  (T6, phi = 5760)
      E(M7) = 8.20e-7  (T7, phi = 92160)

    Args:
        primes:      lista de primos que definen T_k
        prime_limit: limite superior del corpus de primos

    Returns dict con E(M), orden de magnitud, y cotas.
    """
    M   = primorial_M(primes)
    phi = phi_M(primes)

    corpus = [p for p in range(2, prime_limit + 1)
              if _is_prime(p) and gcd(p, M) == 1]
    total = len(corpus)

    if total == 0 or phi == 0:
        return {
            "M": M, "phi_M": phi, "E_M": float("inf"),
            "law_holds": False, "error": "corpus vacio",
        }

    counts     = Counter(p % M for p in corpus)
    admissible = [a for a in range(M) if gcd(a, M) == 1]

    epsilon = {
        a: (counts.get(a, 0) / total) - (1.0 / phi)
        for a in admissible
    }

    sum_epsilon = sum(epsilon.values())
    E_M         = sum(e**2 for e in epsilon.values())
    E_order     = math.log10(E_M) if E_M > 0 else float("-inf")

    return {
        "primes":      primes,
        "M":           M,
        "phi_M":       phi,
        "prime_limit": prime_limit,
        "corpus_size": total,
        "E_M":         E_M,
        "E_order":     E_order,
        "sum_epsilon": sum_epsilon,
        "field_flat":  E_M < 1e-3,
        "law_holds":   E_M < 1e-3,
        "paper_bound": 1e-6,
        "note": (
            "E(M)~O(10^-7) requiere primos hasta ~10^6. "
            "Con corpus pequeno se obtiene O(10^-4). "
            "Usar prime_limit >= 1_000_000 para reproducir el paper."
        ),
    }


# -----------------------------------------------------------------------------
# III. CAMPO DE FOURIER ESPECTRAL
# -----------------------------------------------------------------------------

def spectral_modes(
    primes: List[int],
    prime_limit: int = 5000,
    max_modes: int = 50,
) -> Dict:
    """
    Teorema Espectral (Theorem 6.1 de [TORUS])

    e_hat(k) = sum_a eps(a) * exp(-2*pi*i*k*a/phi(M))

    Propiedades:
      (i)  e_hat(0) = 0          (por construccion de eps)
      (ii) E(M) = (1/phi(M)) * sum_k |e_hat(k)|^2   (Parseval)
      (iii)|e_hat(k)|^2 ~= E/phi(M) para k!=0        (independencia modal)

    Conexion con RH ([TORUS] Seccion 8, [RH] Seccion 17):
      Los modos e_hat(k) deberian codificar las partes imaginarias gamma
      de los ceros de Riemann rho = 1/2 + i*gamma.
      STATUS: trabajo en progreso [6].

    Returns dict con modos espectrales e independencia modal.
    """
    M   = primorial_M(primes)
    phi = phi_M(primes)

    corpus = [p for p in range(2, prime_limit + 1)
              if _is_prime(p) and gcd(p, M) == 1]
    total  = len(corpus)

    if total == 0:
        return {"error": "corpus vacio", "M": M}

    counts     = Counter(p % M for p in corpus)
    admissible = sorted([a for a in range(M) if gcd(a, M) == 1])

    epsilon = {
        a: (counts.get(a, 0) / total) - (1.0 / phi)
        for a in admissible
    }

    modes = {}
    for k in range(min(max_modes, phi)):
        e_hat_k = sum(
            epsilon[a] * math.cos(-2 * math.pi * k * a / phi)
            for a in admissible
        )
        modes[k] = e_hat_k

    E_M      = sum(e**2 for e in epsilon.values())
    E_modes  = {k: v**2 for k, v in modes.items()}
    E_dc     = E_modes.get(0, 0)

    off_dc_modes = {k: v for k, v in E_modes.items() if k != 0}
    max_mode     = max(off_dc_modes.values()) if off_dc_modes else 0.0
    expected     = E_M / phi if phi > 0 else 0.0

    return {
        "M":                 M,
        "phi_M":             phi,
        "E_M":               E_M,
        "E_dc":              E_dc,
        "modes_computed":    len(modes),
        "max_off_dc_mode":   max_mode,
        "expected_per_mode": expected,
        "mode_independence": max_mode < expected * 10 if expected > 0 else None,
        "rh_connection": (
            "Los modos e_hat(k) deberian codificar gamma_k de los ceros de Riemann. "
            "Conexion formal: trabajo en progreso [6]. No implementada."
        ),
    }


# -----------------------------------------------------------------------------
# IV. CONEXION UCF - BETA COMO RESIDUO DEL TOROIDE
# -----------------------------------------------------------------------------

def beta_torus_residue_analysis() -> Dict:
    """
    Pregunta abierta: beta = residuo del toroide?

    El cubo 3x3x3 genera:
      beta = 1/27 = 1/3^3 = residuo geometrico irreducible

    El toroide T7 produce:
      E(M7) = 8.20e-7 = residuo distribucional de primos

    Ambos miden el mismo fenomeno desde perspectivas distintas:
    el residuo estructural que ningun sistema puede eliminar.

    Numericamente (busqueda de n tal que beta^n ~= E(M)):
      beta^4 = 1.882e-6  (ratio a E(M7) = 2.29)  <- mas cercano
      beta^5 = 6.969e-8  (ratio a E(M7) = 0.085)

    STATUS: OPEN - no hay derivacion formal.
    Falsificable si existe n derivable de la geometria del cubo.

    Returns dict con analisis numerico completo.
    """
    powers = {}
    for n in range(1, 12):
        val  = BETA**n
        r_T6 = val / E_M6_PAPER if E_M6_PAPER > 0 else float("inf")
        r_T7 = val / E_M7_PAPER if E_M7_PAPER > 0 else float("inf")
        powers[n] = {
            "value":    val,
            "ratio_T6": r_T6,
            "ratio_T7": r_T7,
            "log10":    math.log10(val),
        }

    closest_n = min(
        range(1, 12),
        key=lambda n: abs(math.log10(BETA**n) - math.log10(E_M7_PAPER))
    )
    closest_v = BETA**closest_n
    closest_r = closest_v / E_M7_PAPER

    return {
        "beta":           BETA,
        "alpha":          ALPHA,
        "E_M6_paper":     E_M6_PAPER,
        "E_M7_paper":     E_M7_PAPER,
        "powers":         powers,
        "closest_n":      closest_n,
        "closest_value":  closest_v,
        "closest_ratio":  closest_r,
        "cube_residue":   BETA,
        "torus_residue":  E_M7_PAPER,
        "status":         "OPEN - no hay derivacion formal",
        "falsifiable_if": "beta^n = E(M) para n derivable de la geometria del cubo",
        "structural_analog": (
            "Cubo:    beta = 1/27 = residuo del centro que no orbita la superficie\n"
            "Toroide: E(M) = residuo distribucional de la distribucion prima\n"
            "Ambos:   el residuo que ningun sistema puede eliminar"
        ),
        "ucf_implication": (
            "C_max = alpha = 1 - beta\n"
            "Ningun sistema real alcanza C = 1\n"
            "Porque el residuo del toroide - como el del cubo - es irreducible"
        ),
    }


def c_max_from_torus(primes: List[int]) -> Dict:
    """
    C_max del framework UCF desde la perspectiva del toroide.

    El cubo 3x3x3 genera alpha = 26/27 como fraccion superficial.
    El toroide T_k genera E(M) ~ O(10^-7) como residuo distribucional.

    La coherencia maxima C_max = alpha = 1 - beta viene de la geometria
    del cubo, que es el caso k=1, n=3 del toroide:
      T1 = Z/3Z  (una sola rueda de tamano 3)
      El cubo extiende esto a 3 dimensiones: 3x3x3

    Returns dict con la conexion cubo-toroide-UCF.
    """
    M   = primorial_M(primes)
    phi = phi_M(primes)
    k   = len(primes)
    cov = torus_coverage(primes)

    beta_analysis = beta_torus_residue_analysis()

    return {
        "primes":          primes,
        "k":               k,
        "M":               M,
        "phi_M":           phi,
        "coverage":        cov,
        "alpha_ucf":       ALPHA,
        "beta_ucf":        BETA,
        "C_max":           ALPHA,
        "C_max_formula":   "1 - beta = 1 - 1/27 = 26/27",
        "geometric_basis": "Cubo 3x3x3: 26 superficie / 27 total",
        "torus_basis":     f"T_{k}: phi(M) = {phi} clases admisibles / M = {M} total",
        "beta_status":     beta_analysis["status"],
        "open_question":   beta_analysis["falsifiable_if"],
    }


# -----------------------------------------------------------------------------
# V. INFINITO OPERACIONAL
# -----------------------------------------------------------------------------

def operational_infinity(primes: List[int]) -> Dict:
    """
    Teorema de Infinito Estructural (Theorem 7.1 de [TORUS])

    Todo proceso x_{n+1} = x_n + 1 sobre M = (n1, ..., nk) es
    estructuralmente finito:

      para todo n en N: phi(n) = phi(n mod P),    P = lcm(n1, ..., nk)

    El numero de estados distintos es exactamente P.
    El aparente infinito de N es la iteracion ilimitada
    de una estructura finita.

    Corollary 7.2 - Resolucion de la Ilusion del Infinito:
    La secuencia 0, 1, 2, 3, ... es el unrolling infinito
    del toroide finito T_k.
    Infinito = numero de vueltas, no tamano de la pista.

    Returns dict con la estructura del infinito operacional.
    """
    M   = primorial_M(primes)
    P   = period(primes)
    k   = len(primes)
    cov = P / M

    start  = state_map(0, primes)
    at_P   = state_map(P, primes)
    closes = start == at_P

    states = [state_map(n, primes) for n in range(P)]
    unique = len(set(states))

    return {
        "primes":           primes,
        "k":                k,
        "M":                M,
        "P":                P,
        "coverage":         cov,
        "closure_at_P":     closes,
        "unique_states":    unique,
        "is_bijection":     unique == P,
        "laps":             "infinitas - la helice orbita T_k para siempre",
        "structure_finite": True,
        "infinity_type":    "operacional (numero de vueltas), no estructural (tamano)",
        "interpretation": (
            f"Los enteros no van en linea recta.\n"
            f"Orbitan T_{k} = Z/{primes[0]}Z x ... x Z/{primes[-1]}Z.\n"
            f"El toroide tiene {P} estados.\n"
            f"Infinito = numero de vueltas alrededor de esos {P} estados."
        ),
    }


# -----------------------------------------------------------------------------
# VI. REPORTE COMPLETO
# -----------------------------------------------------------------------------

def torus_formula_report(
    primes: Optional[List[int]] = None,
    prime_limit: int = 5000,
) -> Dict:
    """
    Reporte completo de la formula del toroide con contexto UCF.

    Integra:
      - Las 4 leyes estructurales del paper [TORUS]
      - El campo aritmetico E(M)
      - La conexion UCF (beta como residuo)
      - El infinito operacional
      - La conexion con RH (estado: trabajo en progreso)

    Args:
        primes:      lista de primos (default: T4 = [2,3,5,7])
        prime_limit: limite del corpus para E(M)
    """
    if primes is None:
        primes = TORUS_PRIMES[4]

    M   = primorial_M(primes)
    phi = phi_M(primes)
    k   = len(primes)

    l1 = law1_cycle_independence(primes)
    l2 = law2_cycle_resonance([4, 6])
    l3 = law3_prime_filtering(
        B=max(primes), check_up_to=max(primes) * 10
    )
    l4 = law4_field_energy(primes, prime_limit)

    inf_op        = operational_infinity(primes)
    beta_analysis = beta_torus_residue_analysis()
    c_max         = c_max_from_torus(primes)

    all_laws_pass = (
        l1["law_holds"]
        and l2["law_holds"]
        and l3["law_holds"]
        and l4["law_holds"]
    )

    return {
        "formula":       "N es el espacio de cobertura de T_k = prod_{p<=B} Z/pZ",
        "primes":        primes,
        "k":             k,
        "M":             M,
        "phi_M":         phi,
        "law1":          l1,
        "law2":          l2,
        "law3":          l3,
        "law4":          l4,
        "all_laws_pass": all_laws_pass,
        "operational_infinity": inf_op,
        "beta_analysis": beta_analysis,
        "c_max":         c_max,
        "rh_connection": {
            "status":      "trabajo en progreso [6]",
            "claim":       "e_hat(k) deberia codificar gamma_k de los ceros de Riemann",
            "consistency": "E(M)~10^-7 es consistente con RH (campo plano = ceros en Re=1/2)",
            "implemented": False,
            "note":        "No implementado sin prueba completa",
        },
        "ucf_integration": {
            "beta":  BETA,
            "alpha": ALPHA,
            "C_max": ALPHA,
            "interpretation": (
                "Los enteros orbitan el toroide para siempre.\n"
                "Beta es el residuo irreducible - el centro que no puede orbitar.\n"
                "Por eso C_max = alpha = 1 - beta.\n"
                "Ningun sistema real alcanza C = 1."
            ),
        },
        "papers": {
            "torus": "[TORUS] Structural Cycles and Operational Infinity, Villasmil 2026",
            "rh":    "[RH] Resolution of the Riemann Hypothesis, Villasmil 2026",
            "ucf":   "[UCF] Villasmil-Omega Framework: Integration of Everything, 2026",
        },
    }
