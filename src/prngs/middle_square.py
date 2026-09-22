def generar_uniformes(semilla, cantidad, digitos=8):
    x = semilla % (10 ** digitos)
    valores = []
    for i in range(cantidad):
        cuadrado = str(x * x).zfill(digitos * 2)
        inicio = (len(cuadrado) - digitos) // 2
        x = int(cuadrado[inicio:inicio + digitos])
        if x == 0:
            x = (semilla * 6151 + i * 7919 + 1) % (10 ** digitos)
        valores.append(x / (10 ** digitos))
    return valores


SEMILLA_DEFECTO = 57282719
