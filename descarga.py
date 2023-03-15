import requests
import schedule
import time

def descargar_archivo_csv():
    url = 'blob:https://www.cboe.com/200784d7-c5dc-4f85-b375-256302c894f5'
    respuesta = requests.get(url)

    if respuesta.status_code == 200:
        with open('archivo.csv', 'wb') as f:
            f.write(respuesta.content)
        print('Archivo CSV descargado exitosamente.')
    else:
        print('No se pudo descargar el archivo CSV.')

# Programa la descarga cada 3 horas empezando a las 10:00 am
schedule.every().day.at('10:00').do(descargar_archivo_csv)
schedule.every().day.at('13:00').do(descargar_archivo_csv)
schedule.every().day.at('16:00').do(descargar_archivo_csv)
schedule.every().day.at('19:00').do(descargar_archivo_csv)

while True:
    schedule.run_pending()
    time.sleep(1)
