# Tarea 2 - Numeros Pseudoaleatorios y Metodos de Monte Carlo

Didvin Nohel Estrada Pineda, carne 14092. Curso Libre de Configuracion 2: Analisis de Datos, Universidad del Istmo.

## Estructura

```
src/prngs/         generadores pseudoaleatorios (LCG, cuadrados medios, Mersenne Twister,
                    Blum Blum Shub, RANDU) y run_part1.py, que genera todas las figuras
                    y estadisticos de la Parte 1
src/montecarlo/     estimador de Monte Carlo y los scripts de la Parte 2:
                    integrales_1d.py, volumen_alta_dim.py, reduccion_varianza.py, caso_randu.py
report/report.tex   documento con la investigacion y el analisis
report/report.pdf   documento compilado
report/figures/     figuras generadas por los scripts (incluye figures/derivaciones/,
                    con las fotos de las derivaciones a mano de la seccion 3.1)
```

## Como correr

Instalar dependencias (Python 3.12):

```
pip install -r requirements.txt
```

Cada script se corre desde su propia carpeta y deja las figuras en `report/figures/`. Las semillas usadas quedan fijas dentro de cada archivo, asi que dos corridas dan exactamente el mismo resultado:

```
cd src/prngs && python3 run_part1.py
cd ../montecarlo
python3 integrales_1d.py
python3 volumen_alta_dim.py
python3 reduccion_varianza.py
python3 caso_randu.py
```

El documento ya viene compilado en `report/report.pdf`.
