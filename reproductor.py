from os import listdir
from os.path import isfile, join
import threading, time
import requests
import json

MODO = "kafka"

if MODO == "mqtt":
    import paho.mqtt.client as mqtt
elif MODO == "kafka":
    from kafka import KafkaProducer

class Camion(threading.Thread):

    def __init__(self, camion,  time, data, mode = ""):
        super(Camion, self).__init__()
        self.camion = camion
        self.time = time
        self.data = data
        self.mode = mode

        if mode == 'mqtt':
            self.client = mqtt.Client()
            self.client.connect("127.0.0.1", 8000, 60)
        elif mode == 'kafka':
            self.producer = KafkaProducer(bootstrap_servers='localhost:9092')

    def run(self):
        for entry in self.data:
            if self.mode == "rest":
                if entry != "-":
                    self.enviar_request_response(entry)
            elif self.mode == "mqtt":
                if entry != "-":
                    self.enviar_mqtt(entry)
            elif self.mode == "kafka":
                self.enviar_kafka(entry)
            else:
                print("[{0}] {1}".format(self.camion, entry))

            time.sleep(self.time)

        print("[{0}] Fin de simulacion".format(self.camion))

    
    def enviar_request_response(self, entry):
        parts = entry.split(",")
        data = {
            "timestamp": time.time(),
            "latitud": float(parts[0]),
            "longitud": float(parts[1]),
            "velocidad": int(parts[2]),
            "id_vehiculo": self.camion
        }

        response = requests.post("http://localhost:5000/gps", data)
        if response.status_code == 200:
            print("{0} envio datos".format(self.camion))
        else:
            print("{0} no pudo enviar datos".format(self.camion))
       

    def enviar_mqtt(self, entry):
        parts = entry.split(",")
        data = json.dumps({
            "timestamp": time.time(),
            "latitud": float(parts[0]),
            "longitud": float(parts[1]),
            "velocidad": int(parts[2]),
            "id_vehiculo": self.camion
        })

        self.client.publish("gps", payload=data, qos=0, retain=False)

    def enviar_kafka(self, entry):
        if entry != "-":
            parts = entry.split(",")
            data = json.dumps({
                "timestamp": time.time(),
                "latitud": float(parts[0]),
                "longitud": float(parts[1]),
                "velocidad": int(parts[2]),
                "id_vehiculo": self.camion
            })
        else:
            data = entry

        self.producer.send("gps-data-gateway", value=data.encode('utf-8'))
        self.producer.flush()

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
    c = Camion(camion, intervalo, valores, MODO)
    c.start()
    time.sleep(1)
