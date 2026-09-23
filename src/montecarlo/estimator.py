import math


def estimar_integral_1d(f, a, b, uniformes):
    n = len(uniformes)
    valores = [f(a + (b - a) * u) for u in uniformes]
    promedio = sum(valores) / n
    varianza = sum((v - promedio) ** 2 for v in valores) / (n - 1)
    estimado = (b - a) * promedio
    error_estandar = (b - a) * math.sqrt(varianza / n)
    margen = 1.959964 * error_estandar
    return estimado, (estimado - margen, estimado + margen), error_estandar


def intervalo_confianza_proporcion(exitos, n, z=1.959964):
    p = exitos / n
    error_estandar = math.sqrt(p * (1 - p) / n)
    margen = z * error_estandar
    return p, (p - margen, p + margen), error_estandar
