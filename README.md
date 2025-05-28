# Trabajo Final

**Iñigo Murga, Mikel García y Jon Cañadas**

## Explicación

Este proyecto consiste en realizar todas las fases dadas en la asignatura en un solo reto. Para ello hemos pensado en un mantenimiento predictivo en cuanto a unas máquinas siguiendo los siguientes pasos:

1. Captura

Al comenzar, echamos un vistazo en kaggle para analizar qué ejemplos de datasets en cuanto a mantenimiento predictivo existen. Seguidamente, procedimos a elegir qué variable queríamos para nuestro proyecto, ya que es la base del mismo. Por último, creamos un script de python con el cual se generan los datos de los sensores de las máquinas para poder realizar el monitoreo en tiempo real.

2. Envío

Los datos generados por los sensores había que enviarlos, por lo que escogimos mqtt como un buen método de envío puesto que es el más utilizado en cuanto a sensorica en la vida real. Los datos generados se envían a un script suscriptor donde se seguirá con las demás fases.

3. Procesamiento

Cuando los datos llegan a el suscriptor, son procesados a través del uso de pydantic para evitar la persistencia de datos nulos, vacíos o fuera de lógica en cuanto a string, integer, ...

4. Persistencia

Para persistir los datos hemos decidido utilizar elastic puesto que es la opción más óptima para posteriormente utilizar kibana para la visualización.

5. Visualización

Para visualizar los datos hemos utilizado kibana, donde hemos creado un dashboard con la monitorización en tiempo real de todos los sensores de cada máquina para visualizar la aparición de anomalías.

6. Análisis

Por último, hemos tenido que crear un script para generar datos históricos de las máquinas y posteriormente analizarlas. Esta parte se ha realizado con la creación de un dashboard con diversos gráficos.


## Instalación

1. Clonar el repositorio:
    ```bash
    https://github.com/inigomurga/trabajoFinal-G2.git
    ```
2. Navega al directorio del proyecto:
    ```bash
    cd trabajoFinal-G2
    ```
3. Levantar los contenedores
    ```bash
    docker-compose up -d
    ```

## Uso

1. Abre una terminal de windows y desde la carpeta trabajoFinal-G2 ejecuta el siguiente comando:
    ```bash
    python crear.py
    ```
2. Realiza lo mismo que en el anterior paso pero con este comando:
    ```bash
    python subscriptor.py
    ```
3. Accede a kibana y haz click en "Stack Management" posteriormente en "Saved Objects" y finalmente en "Import" donde seleccionaras el ndjson que esta en la carpeta trabajoFinal-G.

4. Finalemente haz click en "Dashboards" donde estaran tanto el dashboard de monitoreo como el de analisis histórico.
