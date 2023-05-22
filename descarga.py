import requests
from urllib.parse import urlparse

def descargar_archivo(blob_url):
    parsed_url = urlparse(blob_url)
    real_url = parsed_url.fragment

    response = requests.get(real_url)

    if response.status_code == 200:
        content_disposition = response.headers.get('Content-Disposition')
        filename = content_disposition.split('filename=')[1]

        with open(filename, 'wb') as file:
            file.write(response.content)
        print('La descarga se completó correctamente.')
    else:
        print('No se pudo realizar la descarga del archivo.')
