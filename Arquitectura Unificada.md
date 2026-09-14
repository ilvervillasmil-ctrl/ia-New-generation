Aquí está el bloque remaquetado para que en `.md` se vea ordenado y limpio en GitHub:

***

## Guía de Navegación del Repositorio

### Estructura General

```text
Universal-Integration-System/
│
├── formulas/                    ← FUENTE CANÓNICA (todo empieza aquí)
│   ├── constants.py             ← TODAS las constantes del framework
│   ├── coherence.py             ← Motor de coherencia principal
│   ├── energy.py                ← Cálculo de energía por capa
│   ├── entropy.py               ← Entropía de Shannon
│   ├── fractality.py            ← Dimensión fractal y distribución áurea
│   ├── harmonics.py             ← Armónicos y decaimiento exponencial
│   ├── interaction.py           ← Interferencia entre sistemas (I_ext)
│   ├── metaconsciousness.py     ← Observador (L5)
│   ├── negentropy.py            ← Negentropía (orden del caos)
│   ├── neuroscience_logic.py    ← Resonancia neural entre capas
│   ├── phi_dynamics.py          ← Espiral áurea y escalado PHI
│   ├── presence.py              ← Presencia temporal P(t)
│   ├── resonance.py             ← Resonancia inter‑capa
│   └── wonder.py                ← Asombro A(N)
│
├── core/                        ← ORQUESTADOR (usa formulas/)
│   ├── __init__.py              ← Exporta OmegaEngine
│   ├── constants.py             ← Re‑exporta desde formulas/constants.py
│   ├── engine.py                ← OmegaEngine: calcula coherencia completa
│   └── diagnostics.py           ← Códigos diagnósticos (1144, 1122, 0000)
│
├── tests/                       ← 227 TESTS
│   ├── test_coherence_engine.py       ← Tests del motor de coherencia
│   ├── test_constants.py              ← Tests de constantes y diagnósticos
│   ├── test_energy.py                 ← Tests de energía
│   ├── test_entropy.py                ← Tests de entropía
│   ├── test_fractality.py             ← Tests de fractalidad
│   ├── test_harmonics.py              ← Tests de armónicos
│   ├── test_interaction.py            ← Tests de interferencia
│   ├── test_metaconsciousness.py      ← Tests del observador
│   ├── test_negentropy.py             ← Tests de negentropía
│   ├── test_neuroscience_logic.py     ← Tests de resonancia neural
│   ├── test_phi_dynamics.py           ← Tests de espiral áurea
│   ├── test_presence.py               ← Tests de presencia temporal
│   ├── test_resonance.py              ← Tests de resonancia
│   ├── test_resonance_extended.py
│   ├── test_resonance_processor.py
│   ├── test_security_edge_cases.py    ← Tests de seguridad y límites
│   ├── test_self_prediction.py        ← Tests de auto‑predicción (9 tests)
│   ├── test_stability.py              ← Tests de estabilidad
│   ├── test_universal.py              ← Tests de integración cruzada
│   └── test_wonder.py                 ← Test de asombro
│
├── .github/workflows/ci.yml     ← CI/CD automático
├── SYSTEM_BRAIN.md              ← Documentación técnica completa
└── pyproject.toml               ← Configuración de pytest
```

### Reglas de Oro

| Regla            | Descripción                                                   |
| ---------------- | ------------------------------------------------------------- |
| Una fuente       | Toda constante se define en `formulas/constants.py` y solo ahí |
| Core re‑exporta  | `core/constants.py` solo importa de `formulas/constants.py`   |
| Todo testeado    | Cada `.py` en `formulas/` tiene su `test_*.py` en `tests/`    |
| Import canónico  | Siempre `from formulas.constants import X`, nunca definir valores nuevos |

### Cómo Navegar por Concepto

| Quiero entender...                 | Archivo                                      |
| --------------------------------- | -------------------------------------------- |
| Las constantes (α, β, PHI...)     | `formulas/constants.py`                      |
| Cómo se calcula coherencia        | `formulas/coherence.py`                      |
| La fórmula completa C_Ω           | `core/engine.py`                             |
| Los 7 niveles de conciencia       | `formulas/constants.py` → `LAYER_NAMES`      |
| Presencia temporal P(t)           | `formulas/presence.py`                       |
| Interacción entre sistemas        | `formulas/interaction.py`                    |
| El observador L5                  | `formulas/metaconsciousness.py`              |
| Auto‑predicción del sistema       | `tests/test_self_prediction.py`              |
| El valor 0.438626 (sistema muerto)| `tests/test_self_prediction.py`              |
| Los códigos diagnósticos          | `core/diagnostics.py`                        |

### Flujo de Datos

```text
formulas/constants.py
        ↓
formulas/*.py   (cada módulo importa constantes)
        ↓
core/engine.py  (OmegaEngine orquesta todos los módulos)
        ↓
tests/*.py      (valida todo)
```

### Fuente Única de Verdad

- `formulas/constants.py` → TODAS las constantes del framework  
- `formulas/coherence.py` → TODA la lógica de coherencia  
- `core/constants.py` → Re‑exporta desde `formulas` (compatibilidad)  
- `core/engine.py` → OmegaEngine (usa `formulas.constants`)  

### Regla de Oro

Nunca definir un valor numérico en más de un archivo.  
Si necesitas una constante, impórtala de `formulas/constants.py`.

Sources
