import os
import sys
import math
import random

import numpy as np
import matplotlib.pyplot as plt

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "prngs"))
import lcg

from estimator import estimar_integral_1d

CARPETA_FIGURAS = os.path.join(os.path.dirname(__file__), "..", "..", "report", "figures")
os.makedirs(CARPETA_FIGURAS, exist_ok=True)

SEMILLA = 20250922

INTEGRALES = {
    "a": {
        "f": lambda x: math.sin(math.pi * x),
        "a": 0.0,
        "b": 1.0,
        "valor_real": 2.0 / math.pi,
        "nombre": "sin(pi x) en [0,1]",
    },
    "b": {
        "f": lambda x: math.exp(-x * x / 2.0) / math.sqrt(2.0 * math.pi),
        "a": 0.0,
        "b": 2.0,
        "valor_real": 0.5 * (math.erf(2.0 / math.sqrt(2.0)) - math.erf(0.0)),
        "nombre": "normal estandar en [0,2]",
    },
}

N_VALORES = np.unique(np.logspace(1, 6, 25).astype(int))


def uniformes_random(rng, n):
    return [rng.random() for _ in range(n)]


def uniformes_lcg(n):
    return lcg.generar_uniformes(SEMILLA, n)


def estudio_convergencia(clave):
    datos = INTEGRALES[clave]
    f, a, b, valor_real = datos["f"], datos["a"], datos["b"], datos["valor_real"]

    rng = random.Random(SEMILLA)
    errores_estandar = []
    for n in N_VALORES:
        u = uniformes_random(rng, int(n))
        estimado, ic, _ = estimar_integral_1d(f, a, b, u)
        errores_estandar.append(abs(estimado - valor_real))

    x = int(lcg.SEMILLA_DEFECTO)
    contador = 0
    errores_propio = []
    for n in N_VALORES:
        u = lcg.generar_uniformes((SEMILLA + contador) % (2 ** 32), int(n))
        contador += int(n)
        estimado, ic, _ = estimar_integral_1d(f, a, b, u)
        errores_propio.append(abs(estimado - valor_real))

    log_n = np.log10(N_VALORES.astype(float))
    log_err = np.log10(errores_estandar)
    pendiente, intercepto = np.polyfit(log_n, log_err, 1)

    plt.figure(figsize=(5.5, 4))
    plt.loglog(N_VALORES, errores_estandar, "o-", label="random estandar", color="#4c72b0")
    plt.loglog(N_VALORES, errores_propio, "o-", label="LCG propio", color="#c44e52")
    plt.loglog(N_VALORES, N_VALORES.astype(float) ** -0.5 * errores_estandar[0] * N_VALORES[0] ** 0.5,
               "--", color="gray", label="pendiente -1/2 de referencia")
    plt.xlabel("N")
    plt.ylabel("error absoluto |I_N - I|")
    plt.title(f"Convergencia, integral ({clave})")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(CARPETA_FIGURAS, f"convergencia_{clave}.png"), dpi=150)
    plt.close()

    return pendiente


def reportar_estimacion_final(clave, n=1_000_000):
    datos = INTEGRALES[clave]
    f, a, b, valor_real = datos["f"], datos["a"], datos["b"], datos["valor_real"]
    rng = random.Random(SEMILLA + 999)
    u = uniformes_random(rng, n)
    estimado, ic, error_estandar = estimar_integral_1d(f, a, b, u)
    print(f"integral ({clave}) [{datos['nombre']}]")
    print(f"  valor real       = {valor_real:.6f}")
    print(f"  estimado (N={n}) = {estimado:.6f}")
    print(f"  IC 95%           = ({ic[0]:.6f}, {ic[1]:.6f})")
    print(f"  error absoluto   = {abs(estimado - valor_real):.6f}")


if __name__ == "__main__":
    for clave in ["a", "b"]:
        reportar_estimacion_final(clave)
        pendiente = estudio_convergencia(clave)
        print(f"  pendiente log-log = {pendiente:.4f}")
        print()
