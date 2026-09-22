P = 300007
Q = 300163
M = P * Q


def generar_uniformes(semilla, cantidad, m=M):
    x = semilla % m
    valores = []
    for _ in range(cantidad):
        x = (x * x) % m
        valores.append(x / m)
    return valores


def generar_bits(semilla, cantidad_bits, m=M):
    x = semilla % m
    bits = []
    for _ in range(cantidad_bits):
        x = (x * x) % m
        bits.append(x & 1)
    return bits


SEMILLA_DEFECTO = 987654323
