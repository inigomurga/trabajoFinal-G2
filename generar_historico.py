import csv
import random
import pandas as pd
from datetime import datetime, timedelta

# Función existente
def generar_dato(sensor, valor_anterior):
    if random.random() < 0.03:
        return None
    if random.random() < 0.03:
        if sensor == "temperatura":
            return round(random.uniform(150, 300), 2)
        elif sensor == "vibracion":
            return round(random.uniform(20, 50), 2)
        elif sensor == "corriente_electrica":
            return round(random.uniform(100, 200), 2)
        elif sensor == "rpm_cabezal":
            return random.randint(10000, 20000)

    if sensor == "temperatura":
        if valor_anterior is None or valor_anterior > 149:
            return round(random.uniform(20, 100), 2)
        elif valor_anterior > 110:
            return valor_anterior - 8.33
        else:
            return round(valor_anterior + random.choice([-1.33, 1.34]), 2)

    elif sensor == "vibracion":
        if valor_anterior is None or valor_anterior > 19:
            return round(random.uniform(0, 10), 2)
        elif valor_anterior > 13:
            return valor_anterior - 3.3
        else:
            return round(valor_anterior + random.choice([-0.3, 0.4]), 2)

    elif sensor == "corriente_electrica":
        if valor_anterior is None or valor_anterior > 99:
            return round(random.uniform(0, 50), 2)
        elif valor_anterior > 65:
            return valor_anterior - 8.17
        else:
            return round(valor_anterior + random.choice([-1.17, 1.18]), 2)

    elif sensor == "rpm_cabezal":
        if valor_anterior is None or valor_anterior > 9999:
            return random.randint(500, 3000)
        elif valor_anterior > 3600:
            return valor_anterior - 333
        else:
            return valor_anterior + random.choice([-33, 33])
    return None

# Generar CSV con timestamps
def generar_csv(nombre_archivo="historico_sensores.csv", num_filas=50000):
    campos = ["temperatura", "vibracion", "corriente_electrica", "rpm_cabezal"]
    maquinas = [i + 1 for i in range(5)]
    valores_anteriores = {campo: None for campo in campos}
    datos = []

    # Timestamp inicial
    timestamp_inicial = datetime.now()

    for i in range(num_filas):
        id_maquina = random.choice(maquinas)
        fila = {
            "fila": i + 1,
            "timestamp": timestamp_inicial + timedelta(seconds=i),
            "id_maquina": id_maquina
        }
        for sensor in campos:
            valor = generar_dato(sensor, valores_anteriores[sensor])
            valores_anteriores[sensor] = valor
            fila[sensor] = valor
        datos.append(fila)

    # Crear y guardar DataFrame
    df = pd.DataFrame(datos)
    df.to_csv(nombre_archivo, index=False)
    print(f"Archivo CSV '{nombre_archivo}' generado con {num_filas} filas y timestamps por segundo.")

# Ejecutar
if __name__ == "__main__":
    generar_csv()
