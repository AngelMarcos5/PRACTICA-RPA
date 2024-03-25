import requests
from datetime import datetime, timedelta
import csv

# Configuración inicial
clave_api = "_4MMKz3eDiSwUtRqqVi62W-a8XDVmoEgqa0o_bGC_o9vjOvROu"
id_estacion = "TF164"
fecha_final = datetime.today() - timedelta(days=1)
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
        escritor.writerow(['Fecha y Hora', 'Radiacion'])

        for i, registro in enumerate(datos['Datos']):
            # Ajustar la hora para cada entrada, asumiendo que cada entrada es de 30 minutos
            fecha_hora_ajustada = datetime.strptime(registro['Fecha'], '%Y-%m-%dT%H:%M:%S')
            fecha_hora_ajustada += timedelta(minutes=30 * i)  # Incrementa 30 minutos por cada registro
            escritor.writerow([fecha_hora_ajustada.strftime('%Y-%m-%d %H:%M:%S'), registro.get('Radiacion', 'No Disponible')])

    print(f"Datos guardados en {nombre_archivo_csv}")
else:
    print(f"Error al realizar la solicitud: {respuesta.status_code}, Detalles: {respuesta.text}")


