def generar_uniformes(semilla, cantidad, a=65539, m=2**31):
    x = semilla % m
    if x % 2 == 0:
        x += 1
    valores = []
    for _ in range(cantidad):
        x = (a * x) % m
        valores.append(x / m)
    return valores


def generar_crudos(semilla, cantidad, a=65539, m=2**31):
    x = semilla % m
    if x % 2 == 0:
        x += 1
    crudos = []
    for _ in range(cantidad):
        x = (a * x) % m
        crudos.append(x)
    return crudos


SEMILLA_DEFECTO = 1
