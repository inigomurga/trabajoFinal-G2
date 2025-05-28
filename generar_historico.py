import csv
import random
import pandas as pd
from datetime import datetime, timedelta

# Rangos normales según crear.py
RANGOS = {
    "temperatura": (20, 100),
    "vibracion": (0, 10),
    "corriente_electrica": (0, 50),
    "rpm_cabezal": (500, 3000)
}

def generar_dato(sensor, valor_anterior):
    # Probabilidad de dato nulo
    if random.random() < 0.03:
        return None, False
    # Probabilidad de dato atípico
    if random.random() < 0.1:
        if sensor == "temperatura":
            return round(random.uniform(150, 300), 2), True
        elif sensor == "vibracion":
            return round(random.uniform(20, 50), 2), True
        elif sensor == "corriente_electrica":
            return round(random.uniform(100, 200), 2), True
        elif sensor == "rpm_cabezal":
            return random.randint(10000, 20000), True
    # Dato normal
    if sensor == "temperatura":
        if valor_anterior is None or valor_anterior > 149:
            return round(random.uniform(20, 100), 2), False
        elif valor_anterior > 110:
            return valor_anterior - 8.33, False
        else:
            return round(valor_anterior + random.choice([-1.33, 1.34]), 2), False

    elif sensor == "vibracion":
        if valor_anterior is None or valor_anterior > 19:
            return round(random.uniform(0, 10), 2), False
        elif valor_anterior > 13:
            return valor_anterior - 3.3, False
        elif valor_anterior < 0.5:
            return valor_anterior + 3.3, False
        else:
            return round(valor_anterior + random.choice([-0.3, 0.4]), 2), False

    elif sensor == "corriente_electrica":
        if valor_anterior is None or valor_anterior > 99:
            return round(random.uniform(0, 50), 2), False
        elif valor_anterior > 70:
            return valor_anterior - 8.17, False
        elif valor_anterior < 2:
            return valor_anterior + 4.17, False
        else:
            return round(valor_anterior + random.choice([-1.17, 1.18]), 2), False

    elif sensor == "rpm_cabezal":
        if valor_anterior is None or valor_anterior > 9999:
            return random.randint(500, 3000), False
        elif valor_anterior > 3600:
            return valor_anterior - 333, False
        else:
            return valor_anterior + random.choice([-33, 33]), False
    return None, False

def generar_csv(nombre_archivo="historico_sensores.csv", num_filas=50000):
    campos = ["temperatura", "vibracion", "corriente_electrica", "rpm_cabezal"]
    maquinas = [i + 1 for i in range(5)]
    valores_anteriores = {m: {campo: None for campo in campos} for m in maquinas}
    datos = []

    timestamp_inicial = datetime.now()
    for i in range(num_filas):
        id_maquina = random.choice(maquinas)
        fila = {
            "timestamp": timestamp_inicial - timedelta(minutes=2 * (num_filas - i)),
            "id_maquina": id_maquina
        }
        fallo = False
        tipo_fallo = ""
        for sensor in campos:
            valor_anterior = valores_anteriores[id_maquina][sensor]
            valor, es_atipico = generar_dato(sensor, valor_anterior)
            valores_anteriores[id_maquina][sensor] = valor
            fila[sensor] = valor
            if es_atipico and not fallo:
                fallo = True
                tipo_fallo = sensor
        fila["fallo"] = fallo
        fila["tipo_fallo"] = tipo_fallo
        datos.append(fila)

    df = pd.DataFrame(datos)
    df['fallo'] = df['fallo'].apply(lambda x: 'true' if x else 'false')
    df.to_csv(nombre_archivo, index=False)
    print(f"Archivo CSV '{nombre_archivo}' generado con {num_filas} filas y timestamps por segundo.")

if __name__ == "__main__":
    generar_csv()
