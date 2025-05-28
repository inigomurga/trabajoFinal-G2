import json
import os
import logging
import paho.mqtt.client as mqtt
from elasticsearch import Elasticsearch
from pydantic import BaseModel, Field, ValidationError
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

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
    temperatura: float = Field(..., le=300)
    vibracion: float = Field(..., le=50)
    corriente_electrica: float = Field(..., le=200)
    rpm_cabezal: int = Field(..., le=20000)

# Configuración de email para notificaciones
EMAIL_ENABLED = True
EMAIL_FROM = os.environ.get("EMAIL_FROM")
EMAIL_TO = os.environ.get("EMAIL_TO")
SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))
SMTP_USER = os.environ.get("SMTP_USER", EMAIL_FROM)
SMTP_PASS = os.environ.get("SMTP_PASS")

if EMAIL_ENABLED and not all([EMAIL_FROM, EMAIL_TO, SMTP_USER, SMTP_PASS]):
    raise RuntimeError("Faltan variables de entorno para el envío de email. Revisa tu archivo .env.")

def enviar_alerta_email(asunto, mensaje):
    if not EMAIL_ENABLED:
        return
    try:
        msg = MIMEText(mensaje)
        msg['Subject'] = asunto
        msg['From'] = EMAIL_FROM
        msg['To'] = EMAIL_TO

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(EMAIL_FROM, [EMAIL_TO], msg.as_string())
        logging.info(f"Alerta enviada por email: {asunto}")
    except Exception as e:
        logging.error(f"Error enviando email: {e}")

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
        
        es.index(index=INDEX_NAME, document=dato.model_dump())
        logging.info(f"Guardado en Elasticsearch: {dato.model_dump()}")

        alertas = []
        if dato.temperatura is not None and dato.temperatura > 149:
            alertas.append(f"Temperatura crítica: {dato.temperatura}°C")
        if dato.vibracion is not None and dato.vibracion > 19:
            alertas.append(f"Vibración elevada: {dato.vibracion} mm/s")
        if dato.corriente_electrica is not None and dato.corriente_electrica > 99:
            alertas.append(f"Corriente eléctrica alta: {dato.corriente_electrica} A")
        if dato.rpm_cabezal is not None and dato.rpm_cabezal > 9999:
            alertas.append(f"RPM cabezal fuera de rango: {dato.rpm_cabezal} rpm")

        if alertas:
            asunto = f"ALERTA IoT - Máquina {dato.ID_maquina}"
            mensaje = f"Se han detectado condiciones críticas en la máquina {dato.ID_maquina}:\n" + "\n".join(alertas) + f"\nTimestamp: {dato.timestamp}"
            enviar_alerta_email(asunto, mensaje)

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