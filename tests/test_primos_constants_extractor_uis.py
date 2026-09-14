import math


PRIMOS_PINZA = (
    5, 7, 11, 13, 17, 19, 23,
    29, 31, 37, 41, 43, 47,
)


def _ceil_div(a: int, b: int) -> int:
    """División entera hacia +∞."""
    return -(-a // b)


def _contar_supervivientes_canal(
    inicio: int,
    fin: int,
    signo: int,
) -> tuple[int, int]:
    """
    Cuenta exactamente los supervivientes del canal

        n = 6k + signo

    con signo ∈ {-1, +1}, dentro de [inicio, fin).

    La optimización clave es que para cada primo p no se evalúa
    n % p para cada candidato.

    Se resuelve una sola vez:

        6k + signo ≡ 0 (mod p)

    y después se eliminan de golpe todos los k pertenecientes
    a esa clase residual.
    """

    assert signo in (-1, 1)

    # ----------------------------------------------------------
    # RANGO EXACTO DE k
    #
    # inicio <= 6k + signo < fin
    # ----------------------------------------------------------

    k_inicio = _ceil_div(inicio - signo, 6)
    k_fin = _ceil_div(fin - signo, 6)

    cantidad = k_fin - k_inicio

    if cantidad <= 0:
        return 0, 0

    # 1 = superviviente
    # 0 = eliminado
    #
    # Un byte por candidato.
    vivos = bytearray(b"\x01") * cantidad

    # ----------------------------------------------------------
    # CRIBA MODULAR POR CLASES RESIDUALES
    # ----------------------------------------------------------

    for p in PRIMOS_PINZA:

        # Como gcd(6, p) = 1 para todos nuestros primos,
        # 6 tiene inverso modular módulo p.
        inverso_6 = pow(6, -1, p)

        # 6k + signo ≡ 0 (mod p)
        #
        # k ≡ -signo * 6^{-1} (mod p)
        residuo_k = (-signo * inverso_6) % p

        # Primera posición dentro de nuestro arreglo cuya
        # k pertenece a esa clase residual.
        primer_indice = (
            residuo_k - (k_inicio % p)
        ) % p

        if primer_indice >= cantidad:
            continue

        # Número de posiciones:
        #
        # primer_indice,
        # primer_indice + p,
        # primer_indice + 2p,
        # ...
        numero_eliminados = (
            (cantidad - 1 - primer_indice) // p
        ) + 1

        # El slicing de bytearray se ejecuta internamente,
        # evitando un bucle Python candidato por candidato.
        vivos[primer_indice::p] = (
            b"\x00" * numero_eliminados
        )

    supervivientes = sum(vivos)

    return supervivientes, cantidad


def test_convergencia_estructural_10_200():
    """
    UIS — Auditoría estructural extrema en escala 10^200.

    Valida simultáneamente:

    1. Canal 6k - 1.
    2. Canal 6k + 1.
    3. Supervivencia de la Pinza modular.
    4. Simetría entre ambos canales.
    5. Estabilidad local mediante bloques.
    6. Amplitud máxima de la densidad.
    7. Desviación RMS estructural.

    La criba se ejecuta por clases residuales, no mediante
    millones de operaciones módulo sobre candidatos individuales.
    """

    ESCALA = 10**200
    VENTANA = 10**7
    NUM_BLOQUES = 20

    TOLERANCIA_CANALES = 5e-3
    TOLERANCIA_OSCILACION = 5e-3
    TOLERANCIA_RMS = 2e-3

    inicio = ESCALA
    fin = ESCALA + VENTANA

    ancho_base = VENTANA // NUM_BLOQUES

    supervivientes_total = 0
    estados_total = 0

    supervivientes_mas = 0
    estados_mas = 0

    supervivientes_menos = 0
    estados_menos = 0

    densidades_bloque = []

    print()
    print("=" * 82)
    print("UIS — AUDITORÍA ESTRUCTURAL MODULAR EXTREMA | ESCALA 10^200")
    print("=" * 82)
    print(f"Inicio                 : {inicio}")
    print(f"Fin                    : {fin}")
    print(f"Ventana                 : {VENTANA:,}")
    print(f"Bloques                 : {NUM_BLOQUES}")
    print(f"Módulos                 : {PRIMOS_PINZA}")
    print("-" * 82)

    # ==========================================================
    # AUDITORÍA POR BLOQUES
    # ==========================================================

    for bloque in range(NUM_BLOQUES):

        b_inicio = inicio + bloque * ancho_base

        if bloque == NUM_BLOQUES - 1:
            b_fin = fin
        else:
            b_fin = b_inicio + ancho_base

        # ------------------------------------------------------
        # CANAL 6k - 1
        # ------------------------------------------------------

        vivos_menos, total_menos = (
            _contar_supervivientes_canal(
                b_inicio,
                b_fin,
                -1,
            )
        )

        # ------------------------------------------------------
        # CANAL 6k + 1
        # ------------------------------------------------------

        vivos_mas, total_mas = (
            _contar_supervivientes_canal(
                b_inicio,
                b_fin,
                +1,
            )
        )

        vivos_bloque = (
            vivos_menos
            + vivos_mas
        )

        estados_bloque = (
            total_menos
            + total_mas
        )

        assert estados_bloque > 0, (
            f"UIS — bloque {bloque + 1} "
            "sin estados auditables."
        )

        densidad_bloque = (
            vivos_bloque
            / estados_bloque
        )

        densidades_bloque.append(
            densidad_bloque
        )

        # Acumuladores globales

        supervivientes_menos += vivos_menos
        estados_menos += total_menos

        supervivientes_mas += vivos_mas
        estados_mas += total_mas

        supervivientes_total += vivos_bloque
        estados_total += estados_bloque

        print(
            f"Bloque {bloque + 1:02d}/{NUM_BLOQUES} | "
            f"estados={estados_bloque:>9,} | "
            f"vivos={vivos_bloque:>9,} | "
            f"rho={densidad_bloque:.12f}"
        )

    # ==========================================================
    # DENSIDADES GLOBALES
    # ==========================================================

    assert estados_total > 0
    assert estados_mas > 0
    assert estados_menos > 0

    densidad_global = (
        supervivientes_total
        / estados_total
    )

    densidad_mas = (
        supervivientes_mas
        / estados_mas
    )

    densidad_menos = (
        supervivientes_menos
        / estados_menos
    )

    densidad_media = (
        sum(densidades_bloque)
        / len(densidades_bloque)
    )

    densidad_minima = min(
        densidades_bloque
    )

    densidad_maxima = max(
        densidades_bloque
    )

    amplitud = (
        densidad_maxima
        - densidad_minima
    )

    diferencia_canales = abs(
        densidad_mas
        - densidad_menos
    )

    rms = math.sqrt(
        sum(
            (
                densidad
                - densidad_global
            ) ** 2
            for densidad in densidades_bloque
        )
        / len(densidades_bloque)
    )

    desviacion_maxima = max(
        abs(
            densidad
            - densidad_global
        )
        for densidad in densidades_bloque
    )

    # ==========================================================
    # INFORME
    # ==========================================================

    print("-" * 82)

    print(
        f"Estados auditados       : "
        f"{estados_total:,}"
    )

    print(
        f"Supervivientes          : "
        f"{supervivientes_total:,}"
    )

    print("-" * 82)

    print(
        f"rho global              : "
        f"{densidad_global:.12f}"
    )

    print(
        f"rho 6k + 1              : "
        f"{densidad_mas:.12f}"
    )

    print(
        f"rho 6k - 1              : "
        f"{densidad_menos:.12f}"
    )

    print(
        f"rho media por bloques   : "
        f"{densidad_media:.12f}"
    )

    print("-" * 82)

    print(
        f"rho mínima              : "
        f"{densidad_minima:.12f}"
    )

    print(
        f"rho máxima              : "
        f"{densidad_maxima:.12f}"
    )

    print(
        f"Amplitud                : "
        f"{amplitud:.12e}"
    )

    print(
        f"Diferencia canales      : "
        f"{diferencia_canales:.12e}"
    )

    print(
        f"Desviación máxima       : "
        f"{desviacion_maxima:.12e}"
    )

    print(
        f"RMS estructural         : "
        f"{rms:.12e}"
    )

    print("=" * 82)

    # ==========================================================
    # VALIDACIÓN UIS
    # ==========================================================

    assert supervivientes_total > 0, (
        "UIS — colapso total de la membrana."
    )

    assert supervivientes_mas > 0, (
        "UIS — colapso del canal 6k + 1."
    )

    assert supervivientes_menos > 0, (
        "UIS — colapso del canal 6k - 1."
    )

    assert all(
        d > 0.0
        for d in densidades_bloque
    ), (
        "UIS — bloque sin supervivencia modular."
    )

    assert 0.0 < densidad_global < 1.0, (
        "UIS — densidad global fuera "
        "del dominio estructural."
    )

    assert (
        diferencia_canales
        < TOLERANCIA_CANALES
    ), (
        "\n"
        "UIS — ASIMETRÍA DE CANALES\n"
        f"rho_6k+1 = {densidad_mas:.12f}\n"
        f"rho_6k-1 = {densidad_menos:.12f}\n"
        f"delta    = {diferencia_canales:.12e}\n"
        f"límite   = {TOLERANCIA_CANALES:.12e}"
    )

    assert (
        amplitud
        < TOLERANCIA_OSCILACION
    ), (
        "\n"
        "UIS — OSCILACIÓN ESTRUCTURAL EXCESIVA\n"
        f"rho_min = {densidad_minima:.12f}\n"
        f"rho_max = {densidad_maxima:.12f}\n"
        f"delta   = {amplitud:.12e}\n"
        f"límite  = {TOLERANCIA_OSCILACION:.12e}"
    )

    assert rms < TOLERANCIA_RMS, (
        "\n"
        "UIS — INESTABILIDAD RMS\n"
        f"rms     = {rms:.12e}\n"
        f"límite  = {TOLERANCIA_RMS:.12e}"
    )
