import schedule
import time
import urllib.request
import pytz
from datetime import datetime

# URL de descarga del archivo CSV
CSV_URL = "https://www.cboe.com/e9c12f5b-a451-4607-889d-7846229ba0b7"
CSV_URL_2 = "https://www.cboe.com/80325bb8-8f75-4cc2-b327-a90bd9c9bf5e"



# Zonas horarias para Europa y Chicago
EUROPE_TZ = pytz.timezone('Europe/Madrid')
CHICAGO_TZ = pytz.timezone('America/Chicago')

def descargar_archivo():
    try:
        # Descargar el archivo CSV
        urllib.request.urlretrieve(CSV_URL, "./Operativa/ndx_quotedata.csv")

        # Registrar la descarga exitosa
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Archivo descargado correctamente.")
    except Exception as e:
        # Registrar el error si la descarga falla
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Error durante la descarga del archivo: {str(e)}")

# Programar la tarea para descargar el archivo todos los días a las 9:00 am en Europa
schedule.every().day.at("09:00").do(lambda: descargar_archivo().astimezone(EUROPE_TZ).localize(datetime.now()))

# Programar la tarea para descargar el archivo todos los días a las 9:00 am en Chicago
schedule.every().day.at("09:00").do(lambda: descargar_archivo().astimezone(CHICAGO_TZ).localize(datetime.now()))



def descargar_archivo_2():
    try:
        # Descargar el archivo CSV
        urllib.request.urlretrieve(CSV_URL_2, "./Operativa/spx_quotedata.csv")

        # Registrar la descarga exitosa
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Archivo descargado correctamente.")
    except Exception as e:
        # Registrar el error si la descarga falla
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Error durante la descarga del archivo: {str(e)}")

# Programar la tarea para descargar el archivo todos los días a las 9:00 am en Europa
schedule.every().day.at("09:00").do(lambda: descargar_archivo_2().astimezone(EUROPE_TZ).localize(datetime.now()))

# Programar la tarea para descargar el archivo todos los días a las 9:00 am en Chicago
schedule.every().day.at("09:00").do(lambda: descargar_archivo_2().astimezone(CHICAGO_TZ).localize(datetime.now()))





# Loop para ejecutar las tareas programadas
while True:
    schedule.run_pending()
    time.sleep(1)
