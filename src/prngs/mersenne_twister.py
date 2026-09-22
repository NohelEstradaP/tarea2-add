N = 624
M = 397
MATRIZ_A = 0x9908b0df
MASCARA_ALTA = 0x80000000
MASCARA_BAJA = 0x7fffffff


class MersenneTwister:
    def __init__(self, semilla):
        self.mt = [0] * N
        self.indice = N
        self.mt[0] = semilla & 0xffffffff
        for i in range(1, N):
            self.mt[i] = (1812433253 * (self.mt[i - 1] ^ (self.mt[i - 1] >> 30)) + i) & 0xffffffff

    def _generar_bloque(self):
        for i in range(N):
            y = (self.mt[i] & MASCARA_ALTA) + (self.mt[(i + 1) % N] & MASCARA_BAJA)
            siguiente = self.mt[(i + M) % N] ^ (y >> 1)
            if y % 2 != 0:
                siguiente ^= MATRIZ_A
            self.mt[i] = siguiente
        self.indice = 0

    def siguiente_entero(self):
        if self.indice >= N:
            self._generar_bloque()
        y = self.mt[self.indice]
        y ^= y >> 11
        y ^= (y << 7) & 0x9d2c5680
        y ^= (y << 15) & 0xefc60000
        y ^= y >> 18
        self.indice += 1
        return y

    def siguiente_uniforme(self):
        return self.siguiente_entero() / 4294967296.0


def generar_uniformes(semilla, cantidad):
    gen = MersenneTwister(semilla)
    return [gen.siguiente_uniforme() for _ in range(cantidad)]


SEMILLA_DEFECTO = 5489
