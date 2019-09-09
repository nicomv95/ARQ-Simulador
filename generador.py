import random
import sys

print("Cargando dataset ...")

puntos = []

with open("./datos/puntos.csv") as archivo:
    for linea in archivo:
        if linea:
            linea = linea.replace('\r','').replace('\n','')
            partes = linea.split(',')
            if len(partes) == 2:
                puntos.append((partes[0], partes[1]))\

print("{0} puntos cargados".format(len(puntos)))

script_path = input("script? ")

try:

    camiones = {}
    camion = ""
    velocidad_minima = 0
    velocidad_maxima = 80

    with open(script_path) as archivo:
        for linea in archivo:
            linea = linea.replace('\r','').replace('\n','')

            if linea.startswith("=> camion:"):
                camion = linea.replace("=> camion:", '').strip()
                camiones[camion] = []
            elif linea.startswith("velocidad:"):
                velocidad_maxima = int(linea.replace("velocidad:", '').strip())
            elif linea.startswith("ubicaciones: "):
                cantidad = int(linea.replace("ubicaciones:", '').strip())
                inicio = random.randint(0, len(puntos))
                for i in range(0,cantidad):
                    punto = puntos[inicio]
                    velocidad = random.randint(velocidad_minima, velocidad_maxima)
                    camiones[camion].append("{0},{1},{2}".format( punto[0], punto[1], velocidad))
                    inicio += 1
                    if inicio >= len(puntos):
                        inicio = 0
            elif linea.startswith("sin conexion:"):
                cantidad = int(linea.replace("sin conexion:", '').strip())
                for i in range(0,cantidad):
                    camiones[camion].append("-")

    for camion, valores in camiones.items():
        with open("./simulacion/{0}.txt".format(camion), 'w') as archivo:
            for valor in valores:
                archivo.write("{0}\n".format(valor))




except Exception as ex:
    print("Error al generar los datos, revise el script")
    print("Unexpected error: {0}".format(ex))