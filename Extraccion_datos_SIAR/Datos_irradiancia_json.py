import requests
from datetime import datetime, timedelta

# Configuración inicial
clave_api = "_4MMKz3eDiSwUtRqqVi62W-a8XDVmoEgqa0o_bGC_o9vjOvROu"
id_estacion = "TF164"
fecha_final = datetime.today()
fecha_inicial = fecha_final - timedelta(days=0)

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

    # Procesar y mostrar los datos solicitados
    for i, registro in enumerate(datos['Datos']):
        # Ajustar la fecha y hora para reflejar intervalos de 30 minutos
        fecha_hora_ajustada = datetime.strptime(registro['Fecha'], '%Y-%m-%dT%H:%M:%S')
        fecha_hora_ajustada += timedelta(minutes=30 * i)  # Incrementa 30 minutos por cada registro
        
        # Formatear la fecha ajustada para la impresión
        fecha_hora_str = fecha_hora_ajustada.strftime('%Y-%m-%d %H:%M:%S')
        
        radiacion = registro.get('Radiacion', 'No Disponible')
        temp_media = registro.get('TempMedia', 'No Disponible')
        vel_viento = registro.get('VelViento', 'No Disponible')
        dir_viento = registro.get('DirViento', 'No Disponible')
        
        print(f"Fecha: {fecha_hora_str}, Radiación: {radiacion}, Temp. Media: {temp_media}°C, Vel. Viento: {vel_viento} m/s, Dir. Viento: {dir_viento}°")
else:
    print(f"Error al realizar la solicitud: {respuesta.status_code}, Detalles: {respuesta.text}")


