import json
import os
import logging
import paho.mqtt.client as mqtt
from elasticsearch import Elasticsearch
from pydantic import BaseModel, Field, ValidationError
from datetime import datetime

# Configuración de logs
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "logs.log")
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Conexión a Elasticsearch
es = Elasticsearch("http://localhost:9200")
INDEX_NAME = "sensores"

# Validación con Pydantic específicas
class SensorData(BaseModel):
    ID_maquina: int
    timestamp: datetime
    temperatura: float = Field(..., le=149)
    vibracion: float = Field(..., le=19)
    corriente_electrica: float = Field(..., le=99)
    rpm_cabezal: int = Field(..., le=9999)

# Funciones de MQTT al conectarse
def on_connect(client, userdata, flags, rc):
    print("Conectado con código de resultado "+str(rc))
    client.subscribe("maquinas/datos")

# Funciones del trato del mensaje
def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        dataJson = json.loads(payload)

        dato = SensorData(**dataJson)

        print(f"[Dato validado] {dato}")
        # Guardar en Elasticsearch
        es.index(index=INDEX_NAME, document=dato.model_dump())
        logging.info(f"Guardado en Elasticsearch: {dato.model_dump()}")
    
    except ValidationError as ve:
        logging.warning(f"Dato inválido: {ve}")
    except Exception as e:
        logging.error(f"Error procesando mensaje: {e}")

# Cliente MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)

# Iniciar el bucle de escucha por el canal 
client.loop_forever()