def generar_uniformes(semilla, cantidad, a=1664525, c=1013904223, m=2**32):
    x = semilla % m
    valores = []
    for _ in range(cantidad):
        x = (a * x + c) % m
        valores.append(x / m)
    return valores


def generar_crudos(semilla, cantidad, a=1664525, c=1013904223, m=2**32):
    x = semilla % m
    crudos = []
    for _ in range(cantidad):
        x = (a * x + c) % m
        crudos.append(x)
    return crudos


SEMILLA_DEFECTO = 20250919
