import os
import time
import random
import secrets
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import lcg
import middle_square
import mersenne_twister
import blum_blum_shub
import randu
from stats_tests import prueba_chi_cuadrado_uniformidad, prueba_autocorrelacion_lag1

CARPETA_FIGURAS = os.path.join(os.path.dirname(__file__), "..", "..", "report", "figures")
os.makedirs(CARPETA_FIGURAS, exist_ok=True)

N_MUESTRA = 10000
N_ESPECTRAL = 20000

GENERADORES = {
    "lcg": (lcg, lcg.SEMILLA_DEFECTO),
    "cuadrados_medios": (middle_square, middle_square.SEMILLA_DEFECTO),
    "mersenne_twister": (mersenne_twister, mersenne_twister.SEMILLA_DEFECTO),
    "blum_blum_shub": (blum_blum_shub, blum_blum_shub.SEMILLA_DEFECTO),
    "randu": (randu, randu.SEMILLA_DEFECTO),
}


def guardar_histograma(nombre, valores):
    plt.figure(figsize=(5, 3.5))
    plt.hist(valores, bins=30, range=(0, 1), color="#4c72b0", edgecolor="black", linewidth=0.3)
    plt.title(nombre)
    plt.xlabel("u")
    plt.ylabel("frecuencia")
    plt.tight_layout()
    plt.savefig(os.path.join(CARPETA_FIGURAS, f"hist_{nombre}.png"), dpi=150)
    plt.close()


def guardar_espectral(nombre, valores, elev=25, azim=-60):
    ternas = list(zip(valores[:-2], valores[1:-1], valores[2:]))
    xs = [t[0] for t in ternas]
    ys = [t[1] for t in ternas]
    zs = [t[2] for t in ternas]
    fig = plt.figure(figsize=(5, 5))
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(xs, ys, zs, s=1.5, alpha=0.6, color="#c44e52")
    ax.set_xlabel("u_i")
    ax.set_ylabel("u_i+1")
    ax.set_zlabel("u_i+2")
    ax.set_title(nombre)
    ax.view_init(elev=elev, azim=azim)
    plt.tight_layout()
    plt.savefig(os.path.join(CARPETA_FIGURAS, f"espectral_{nombre}.png"), dpi=150)
    plt.close()


def correr_pruebas():
    resultados = {}
    for nombre, (modulo, semilla) in GENERADORES.items():
        valores = modulo.generar_uniformes(semilla, N_MUESTRA)
        guardar_histograma(nombre, valores)
        chi2, p_chi2 = prueba_chi_cuadrado_uniformidad(valores)
        r, p_r = prueba_autocorrelacion_lag1(valores)
        resultados[nombre] = (semilla, chi2, p_chi2, r, p_r)
        print(f"{nombre}: semilla={semilla} chi2={chi2:.3f} p_chi2={p_chi2:.4f} r_lag1={r:.4f} p_r={p_r:.4f}")

    modulo, semilla = GENERADORES["lcg"]
    guardar_espectral("lcg", modulo.generar_uniformes(semilla, N_ESPECTRAL))

    modulo, semilla = GENERADORES["randu"]
    valores_randu = modulo.generar_uniformes(semilla, N_ESPECTRAL)
    guardar_espectral("randu", valores_randu)
    guardar_espectral("randu_planos", valores_randu, elev=10, azim=50)

    return resultados


def benchmark_generadores():
    cantidad = 100000
    for nombre, (modulo, semilla) in GENERADORES.items():
        t0 = time.perf_counter()
        modulo.generar_uniformes(semilla, cantidad)
        t = time.perf_counter() - t0
        print(f"{nombre}: {t:.4f}s para {cantidad} numeros ({cantidad/t:.0f} num/s)")


def comparar_con_estandar():
    cantidad = 300000

    t0 = time.perf_counter()
    propios = mersenne_twister.generar_uniformes(mersenne_twister.SEMILLA_DEFECTO, cantidad)
    t_propio = time.perf_counter() - t0

    rng = random.Random(mersenne_twister.SEMILLA_DEFECTO)
    t0 = time.perf_counter()
    estandar = [rng.random() for _ in range(cantidad)]
    t_estandar = time.perf_counter() - t0

    gen_seguro = secrets.SystemRandom()
    t0 = time.perf_counter()
    seguros = [gen_seguro.random() for _ in range(cantidad)]
    t_seguro = time.perf_counter() - t0

    chi2_p, p_p = prueba_chi_cuadrado_uniformidad(propios)
    chi2_e, p_e = prueba_chi_cuadrado_uniformidad(estandar)
    chi2_s, p_s = prueba_chi_cuadrado_uniformidad(seguros)

    print(f"mersenne propio:  {t_propio:.4f}s  chi2={chi2_p:.3f}  p={p_p:.4f}")
    print(f"random estandar:  {t_estandar:.4f}s  chi2={chi2_e:.3f}  p={p_e:.4f}")
    print(f"secrets (CSPRNG): {t_seguro:.4f}s  chi2={chi2_s:.3f}  p={p_s:.4f}")


if __name__ == "__main__":
    correr_pruebas()
    print()
    benchmark_generadores()
    print()
    comparar_con_estandar()
