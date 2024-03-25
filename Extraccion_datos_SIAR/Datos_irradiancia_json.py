import requests
from datetime import datetime, timedelta

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

    # Procesar y mostrar los datos de irradiación
    for registro in datos['Datos']:
        print(f"Fecha: {registro['Fecha']}, Radiación: {registro.get('Radiacion', 'No Disponible')}")
else:
    print(f"Error al realizar la solicitud: {respuesta.status_code}, Detalles: {respuesta.text}")
