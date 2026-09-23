import os
import sys
import math

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "prngs"))
import randu
import mersenne_twister

from estimator import intervalo_confianza_proporcion

N_TERNAS = 1_000_000
VALOR_REAL = math.pi / 6.0


def estimar_con_generador(modulo, semilla, n_ternas):
    uniformes = modulo.generar_uniformes(semilla, n_ternas * 3)
    dentro = 0
    for i in range(n_ternas):
        x = uniformes[3 * i]
        y = uniformes[3 * i + 1]
        z = uniformes[3 * i + 2]
        if x * x + y * y + z * z <= 1.0:
            dentro += 1
    return intervalo_confianza_proporcion(dentro, n_ternas)


def distancia_a_planos(modulo, semilla, n):
    u = modulo.generar_uniformes(semilla, n + 2)
    dists = []
    for i in range(n):
        val = 9 * u[i] - 6 * u[i + 1] + u[i + 2]
        dists.append(abs(val - round(val)))
    return sum(dists) / len(dists), max(dists)


def correr():
    p_randu, ic_randu, ee_randu = estimar_con_generador(randu, randu.SEMILLA_DEFECTO, N_TERNAS)
    p_mt, ic_mt, ee_mt = estimar_con_generador(mersenne_twister, mersenne_twister.SEMILLA_DEFECTO, N_TERNAS)

    print(f"valor real pi/6 = {VALOR_REAL:.6f}")
    print()
    print("RANDU")
    print(f"  estimado = {p_randu:.6f}  IC95% = ({ic_randu[0]:.6f}, {ic_randu[1]:.6f})")
    print(f"  error absoluto = {abs(p_randu - VALOR_REAL):.6f}")
    print()
    print("Mersenne Twister")
    print(f"  estimado = {p_mt:.6f}  IC95% = ({ic_mt[0]:.6f}, {ic_mt[1]:.6f})")
    print(f"  error absoluto = {abs(p_mt - VALOR_REAL):.6f}")
    print()

    media_randu, max_randu = distancia_a_planos(randu, randu.SEMILLA_DEFECTO, 100000)
    media_mt, max_mt = distancia_a_planos(mersenne_twister, mersenne_twister.SEMILLA_DEFECTO, 100000)
    print("distancia de 9u_i - 6u_i+1 + u_i+2 al entero mas cercano")
    print(f"  RANDU: media = {media_randu:.10f}  maxima = {max_randu:.10f}")
    print(f"  MT:    media = {media_mt:.6f}  maxima = {max_mt:.6f}")


if __name__ == "__main__":
    correr()
