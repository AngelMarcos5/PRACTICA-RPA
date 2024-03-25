import requests
from datetime import datetime, timedelta
import csv

# Configuración inicial
clave_api = "_4MMKz3eDiSwUtRqqVi62W-a8XDVmoEgqa0o_bGC_o9vjOvROu"
id_estacion = "TF164"
fecha_final = datetime.today()
fecha_inicial = fecha_final - timedelta(days=1)

# Formatear las fechas para la solicitud
fecha_inicial_str = fecha_inicial.strftime('%Y-%m-%d')
fecha_final_str = fecha_final.strftime('%Y-%m-%d')

# Construir la URL de la solicitud con la clave API y el ID de la estación
url = f"https://servicio.mapama.gob.es/apisiar/API/v1/Datos/Horarios/Estacion?Id=TF164&FechaInicial={fecha_inicial_str}&FechaFinal={fecha_final_str}&ClaveAPI={clave_api}"

# Realizar la solicitud
respuesta = requests.get(url)

# Verificar y procesar la respuesta
if respuesta.status_code == 200:
    datos = respuesta.json()
    nombre_archivo_csv = f"C:\\Users\\angel\\Desktop\\MASTER\\TFM\\DATOS_IRRADIANCIA\\datos_irradiancia_{fecha_inicial_str}_a_{fecha_final_str}.csv"

    with open(nombre_archivo_csv, 'w', newline='') as archivo_csv:
        escritor = csv.writer(archivo_csv)
        escritor.writerow(['Fecha', 'Radiacion'])

        # Asumiendo que 'Radiacion' es uno de los campos en la respuesta; ajustar según sea necesario
        for registro in datos['Datos']:
            escritor.writerow([registro['Fecha'], registro.get('Radiacion', 'No Disponible')])

    print(f"Datos guardados en {nombre_archivo_csv}")
else:
    print(f"Error al realizar la solicitud: {respuesta.status_code}, Detalles: {respuesta.text}")

