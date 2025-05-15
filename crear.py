import random
import time
import json
import paho.mqtt.client as mqtt

# Definir los nombres de las máquinas y sensores
maquinas = [f"maquina_{i+1}" for i in range(5)]
sensores = ["temperatura", "vibracion", "corriente_electrica", "rpm_cabezal"]

def generar_dato(sensor):
    # Probabilidad de dato nulo
    if random.random() < 0.03:
        return None
    # Probabilidad de dato atípico
    if random.random() < 0.03:
        if sensor == "temperatura":
            return round(random.uniform(150, 300), 2)  # fuera de rango normal
        elif sensor == "vibracion":
            return round(random.uniform(20, 50), 2)
        elif sensor == "corriente_electrica":
            return round(random.uniform(100, 200), 2)
        elif sensor == "rpm_cabezal":
            return random.randint(10000, 20000)
    # Dato normal
    if sensor == "temperatura":
        return round(random.uniform(20, 100), 2)  # grados Celsius
    elif sensor == "vibracion":
        return round(random.uniform(0, 10), 2)    # mm/s
    elif sensor == "corriente_electrica":
        return round(random.uniform(0, 50), 2)    # amperios
    elif sensor == "rpm_cabezal":
        return random.randint(500, 3000)          # rpm
    return None

# Configuración MQTT
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "maquinas/datos"

client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, 60)

ultimo_dato = None  # Para duplicados

while True:
    datos = []
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    for maquina in maquinas:
        lectura = {"ID": maquina, "timestamp": timestamp}
        for sensor in sensores:
            lectura[sensor] = generar_dato(sensor)
        datos.append(lectura)
    # Probabilidad de duplicar un dato
    if datos and random.random() < 0.05:
        datos.append(datos[-1].copy())
    # Probabilidad de duplicar el último lote entero
    if ultimo_dato and random.random() < 0.02:
        datos.extend([d.copy() for d in ultimo_dato])
    for d in datos:
        client.publish(MQTT_TOPIC, json.dumps(d))
    ultimo_dato = datos
    time.sleep(5)

