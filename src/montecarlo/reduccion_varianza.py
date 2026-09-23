import os
import math
import random

import matplotlib.pyplot as plt

CARPETA_FIGURAS = os.path.join(os.path.dirname(__file__), "..", "..", "report", "figures")
os.makedirs(CARPETA_FIGURAS, exist_ok=True)

SEMILLA = 20250924
N = 2_000_000


def fa(x):
    return math.sin(math.pi * x)


def fb(x):
    return math.exp(-x * x / 2.0) / math.sqrt(2.0 * math.pi)


def varianza_muestral(valores):
    n = len(valores)
    m = sum(valores) / n
    return sum((v - m) ** 2 for v in valores) / (n - 1), m


def montecarlo_simple(f, a, b, uniformes):
    valores = [f(a + (b - a) * u) for u in uniformes]
    var, media = varianza_muestral(valores)
    return var, media


def antitetico(f, a, b, uniformes):
    pares = [(f(a + (b - a) * u) + f(a + (b - a) * (1 - u))) / 2.0 for u in uniformes]
    var, media = varianza_muestral(pares)
    return var, media


def variables_control(f, g, media_g, uniformes, a, b):
    fx = [f(a + (b - a) * u) for u in uniformes]
    gx = [g(a + (b - a) * u) for u in uniformes]
    var_f, media_f = varianza_muestral(fx)
    var_g, media_gx = varianza_muestral(gx)
    n = len(uniformes)
    cov = sum((fx[i] - media_f) * (gx[i] - media_gx) for i in range(n)) / (n - 1)
    c = cov / var_g
    controlados = [fx[i] - c * (gx[i] - media_g) for i in range(n)]
    var_h, media_h = varianza_muestral(controlados)
    correlacion = cov / math.sqrt(var_f * var_g)
    return var_f, var_h, correlacion, c


def correr():
    rng = random.Random(SEMILLA)
    uniformes = [rng.random() for _ in range(N)]

    var_simple_a, _ = montecarlo_simple(fa, 0, 1, uniformes)
    var_anti_a, _ = antitetico(fa, 0, 1, uniformes)
    factor_anti_a = var_simple_a / (2 * var_anti_a)
    print("integral (a), antiteticas")
    print(f"  Var(f(U)) simple    = {var_simple_a:.6f}")
    print(f"  Var(par antitetico) = {var_anti_a:.6f}")
    print(f"  factor de reduccion = {factor_anti_a:.4f}  (speedup efectivo)")
    print()

    var_simple_b, _ = montecarlo_simple(fb, 0, 2, uniformes)
    var_anti_b, _ = antitetico(fb, 0, 2, uniformes)
    factor_anti_b = var_simple_b / (2 * var_anti_b)
    print("integral (b), antiteticas")
    print(f"  Var(f(U)) simple    = {var_simple_b:.6f}")
    print(f"  Var(par antitetico) = {var_anti_b:.8f}")
    print(f"  factor de reduccion = {factor_anti_b:.4f}  (speedup efectivo)")
    print()

    g_lineal = lambda x: x
    var_f, var_h, corr, c = variables_control(fa, g_lineal, 0.5, uniformes, 0, 1)
    factor_lineal = var_f / var_h
    print("integral (a), control variate g(x) = x")
    print(f"  correlacion(f,g) = {corr:.4f}")
    print(f"  c* = {c:.4f}")
    print(f"  factor de reduccion = {factor_lineal:.4f}")
    print()

    g_cuadratico = lambda x: x * (1 - x)
    var_f2, var_h2, corr2, c2 = variables_control(fa, g_cuadratico, 1.0 / 6.0, uniformes, 0, 1)
    factor_cuadratico = var_f2 / var_h2
    print("integral (a), control variate g(x) = x(1-x)")
    print(f"  correlacion(f,g) = {corr2:.4f}")
    print(f"  c* = {c2:.4f}")
    print(f"  factor de reduccion = {factor_cuadratico:.4f}")

    etiquetas = ["antitetica (a)\n[falla]", "antitetica (b)\n[funciona]", "control g=x\n[falla]", "control g=x(1-x)\n[funciona]"]
    factores = [factor_anti_a, factor_anti_b, factor_lineal, factor_cuadratico]
    colores = ["#c44e52", "#55a868", "#c44e52", "#55a868"]

    plt.figure(figsize=(6, 4))
    plt.bar(etiquetas, factores, color=colores)
    plt.axhline(1.0, color="black", linewidth=0.8, linestyle="--")
    plt.yscale("log")
    plt.ylabel("factor de reduccion de varianza (escala log)")
    plt.title("Reduccion de varianza por tecnica")
    plt.tight_layout()
    plt.savefig(os.path.join(CARPETA_FIGURAS, "reduccion_varianza.png"), dpi=150)
    plt.close()


if __name__ == "__main__":
    correr()
