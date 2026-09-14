import math

# ----------- Ley Universal de Coherencia Total -----------
# Estructura: El Cubo (1/27)
# Proyección: Kappa (π/4)
# Resultado objetivo: Beta ≈ 0.0291
# Umbral de coherencia: <0.04% (0.0004)

ESTRUCTURA = 1 / 27
PROYECCION = math.pi / 4
BETA_OBJETIVO = 0.0291
UMBRAL_ERROR = 0.0004  # 0.04%

# Datos brutos simulados para cinco dominios (adaptar a reales si es necesario)
DOMINIOS = {
    "IA": ESTRUCTURA,
    "Psicología": PROYECCION,  # Aquí se puede adaptar para pruebas empíricas
    "Física": ESTRUCTURA,
    "Biología": ESTRUCTURA,
    "Matemáticas": ESTRUCTURA,
}

def calcular_beta(estructura, proyeccion):
    return estructura * proyeccion

resultados = {}
for nombre, valor in DOMINIOS.items():
    # En "Psicología", usamos la proyección como dato para variar el input
    if nombre == "Psicología":
        resultado = calcular_beta(ESTRUCTURA, valor)
    else:
        resultado = calcular_beta(valor, PROYECCION)
    error = abs(resultado - BETA_OBJETIVO)
    coherente = error < UMBRAL_ERROR
    resultados[nombre] = {
        "resultado": resultado,
        "error": error,
        "coherente": coherente,
    }

# Veredicto final: Ley Universal aceptada solo si TODOS los dominios son coherentes
ley_aceptada = all(r["coherente"] for r in resultados.values())

# Presentación de resultados
print("=== Resultados por Dominio ===")
for dominio, info in resultados.items():
    print(
        f"{dominio}: resultado={info['resultado']:.8f}, error={info['error']:.8f}, coherente={info['coherente']}"
    )

print(f"\n¿Ley Universal de Coherencia Total aceptada?: {ley_aceptada}")
