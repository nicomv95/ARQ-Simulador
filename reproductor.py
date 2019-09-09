from os import listdir
from os.path import isfile, join
import threading, time
import json

class Camion(threading.Thread):

    def __init__(self, camion,  time, data, mode = "mqtt"):
        super(Camion, self).__init__()
        self.camion = camion
        self.time = time
        self.data = data
        self.mode = mode

    def run(self):
        for entry in self.data:
            print("[{0}] {1}".format(self.camion, entry))
            time.sleep(self.time)

        print("[{0}] Fin de simulacion".format(self.camion))


print("Cargando datos ...")

mypath = "./simulacion"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

camiones = {}
for path in onlyfiles:
    camion = path.split('/')[-1].replace('.txt', '')

    camiones[camion] = []

    with open("./simulacion/{0}".format(path)) as archivo:
        for linea in archivo:
            linea = linea.replace('\r','').replace('\n','')
            if len(linea)>0:
                camiones[camion].append(linea)

print("Iniciando simulacion para {0} camiones".format(len(camiones)))

intervalo = int(input("intervalo (segs.)? "))
for camion, valores in camiones.items():
    c = Camion(camion, intervalo, valores)
    c.start()
    time.sleep(1)
