import numpy as np
from scipy import stats


def prueba_chi_cuadrado_uniformidad(valores, k=20):
    n = len(valores)
    bordes = np.linspace(0, 1, k + 1)
    observadas, _ = np.histogram(valores, bins=bordes)
    esperadas = np.full(k, n / k)
    estadistico = np.sum((observadas - esperadas) ** 2 / esperadas)
    p_valor = 1 - stats.chi2.cdf(estadistico, df=k - 1)
    return estadistico, p_valor


def prueba_autocorrelacion_lag1(valores):
    u = np.array(valores)
    r, p_valor = stats.pearsonr(u[:-1], u[1:])
    return r, p_valor
