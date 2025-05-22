import random
import time
import json
import paho.mqtt.client as mqtt

# Definir los nombres de las máquinas y sensores
maquinas = [f"maquina_{i+1}" for i in range(5)]
sensores = ["temperatura", "vibracion", "corriente_electrica", "rpm_cabezal"]

ultimos_valores = {m: {s: None for s in sensores} for m in maquinas}

def generar_dato(sensor, valor_anterior):
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
        if valor_anterior is None or valor_anterior > 149:
            return round(random.uniform(20, 100), 2)  # grados Celsius
        elif valor_anterior > 110:
            return valor_anterior - 8.33
        else:
            return round(valor_anterior + random.choice([-1.33, 1.34]), 2)
        
    elif sensor == "vibracion":
        if valor_anterior is None or valor_anterior > 19:
            return round(random.uniform(0, 10), 2)    # mm/s
        elif valor_anterior > 13:
            return valor_anterior - 3.3
        else:
            return round(valor_anterior + random.choice([-0.3, 0.4]), 2)
        
    elif sensor == "corriente_electrica":
        if valor_anterior is None or valor_anterior > 99:
            return round(random.uniform(0, 50), 2)    # amperios
        elif valor_anterior > 65:
            return valor_anterior - 8.17
        else:
            return round(valor_anterior + random.choice([-1.17, 1.18]), 2)
            
    elif sensor == "rpm_cabezal":
        if valor_anterior is None or valor_anterior > 9999:
            return random.randint(500, 3000)          # rpm
        elif valor_anterior > 3600:
            return valor_anterior - 333
        else:
            return valor_anterior + random.choice([-33, 33])
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
            valor_anterior = ultimos_valores[maquina][sensor]
            nuevo_valor = generar_dato(sensor, valor_anterior)
            ultimos_valores[maquina][sensor] = nuevo_valor
            lectura[sensor] = nuevo_valor
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

