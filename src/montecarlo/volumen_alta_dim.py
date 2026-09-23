import os
import sys
import math
import random
import itertools

import numpy as np
import matplotlib.pyplot as plt

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "prngs"))
import lcg

from estimator import intervalo_confianza_proporcion

CARPETA_FIGURAS = os.path.join(os.path.dirname(__file__), "..", "..", "report", "figures")
os.makedirs(CARPETA_FIGURAS, exist_ok=True)

SEMILLA = 20250923
N_PUNTOS = 1_000_000
DIMENSIONES = [2, 5, 10, 20]


def volumen_bola_exacto(d):
    return math.pi ** (d / 2) / math.gamma(d / 2 + 1)


def estimar_volumen_mc(d, n, semilla):
    uniformes = lcg.generar_uniformes(semilla, n * d)
    dentro = 0
    idx = 0
    for _ in range(n):
        suma_cuadrados = 0.0
        for _ in range(d):
            x = -1 + 2 * uniformes[idx]
            idx += 1
            suma_cuadrados += x * x
        if suma_cuadrados <= 1.0:
            dentro += 1
    p, ic, _ = intervalo_confianza_proporcion(dentro, n)
    factor = 2.0 ** d
    if dentro == 0:
        cota_superior = 3.0 / n
        return 0.0, (0.0, cota_superior * factor), dentro
    return p * factor, (ic[0] * factor, ic[1] * factor), dentro


def estimar_volumen_rejilla(d, n_objetivo):
    m = max(2, int(round(n_objetivo ** (1.0 / d))))
    centros = [-1 + (2 * k + 1) / m for k in range(m)]
    dentro = 0
    total = 0
    for combo in itertools.product(centros, repeat=d):
        total += 1
        if sum(c * c for c in combo) <= 1.0:
            dentro += 1
    factor = 2.0 ** d
    return (dentro / total) * factor, total, m


def tabla_maldicion(m=10):
    print(f"puntos necesarios en rejilla con m={m} subdivisiones por eje")
    for d in DIMENSIONES:
        print(f"  d={d}: {m**d:,} puntos")


def correr():
    print("volumen de la bola unitaria: Monte Carlo vs rejilla, N objetivo =", N_PUNTOS)
    for i, d in enumerate(DIMENSIONES):
        real = volumen_bola_exacto(d)
        estimado_mc, ic, dentro = estimar_volumen_mc(d, N_PUNTOS, SEMILLA + i * 7919)
        estimado_rejilla, puntos_rejilla, m = estimar_volumen_rejilla(d, N_PUNTOS)
        error_mc = abs(estimado_mc - real)
        error_rejilla = abs(estimado_rejilla - real)
        print(f"d={d}")
        print(f"  V_d real           = {real:.6g}")
        print(f"  MC: aciertos={dentro}/{N_PUNTOS}  estimado={estimado_mc:.6g}  IC95%={ic}")
        print(f"  MC error absoluto  = {error_mc:.6g}")
        print(f"  rejilla m={m} ({puntos_rejilla:,} puntos)  estimado={estimado_rejilla:.6g}  error={error_rejilla:.6g}")
        print()

    print()
    tabla_maldicion()


def graficar_fraccion_volumen(d_max=20):
    ds = list(range(1, d_max + 1))
    fracciones = [volumen_bola_exacto(d) / 2 ** d for d in ds]
    plt.figure(figsize=(5.5, 4))
    plt.semilogy(ds, fracciones, "o-", color="#4c72b0")
    plt.xlabel("dimension d")
    plt.ylabel("V_d / 2^d")
    plt.title("Fraccion del cubo ocupada por la bola unitaria")
    plt.tight_layout()
    plt.savefig(os.path.join(CARPETA_FIGURAS, "fraccion_volumen.png"), dpi=150)
    plt.close()


if __name__ == "__main__":
    correr()
    graficar_fraccion_volumen()
