import pyautogui
import requests
from datetime import datetime, timedelta
import time
import pyperclip

# Función para abrir Microsoft Word
def abrir_word():
    pyautogui.press('win') # Abrimos el menú de inicio
    time.sleep(2)
    pyautogui.write('Word') # Escribimos 'Word' para buscar la aplicación
    time.sleep(2)
    pyautogui.press('enter') # Abre Microsoft Word
    time.sleep(5)

def escribir_en_word(textos):
    abrir_word()  # Asegura que Word esté abierto antes de escribir
    for texto in textos:
        pyperclip.copy(texto)  # Copia el texto al portapapeles
        pyautogui.hotkey('ctrl', 'v')  # Pega el texto desde el portapapeles
        pyautogui.press('enter')  # Presiona enter para un nuevo párrafo
        time.sleep(1)
    pyautogui.hotkey('ctrl', 'g')  # Inicia el proceso de guardado
    time.sleep(2)
    # Define la ruta completa donde deseas guardar el archivo, incluyendo el nombre del archivo y la extensión
    ruta_completa = r'C:\Users\angel\Desktop\MASTER\2º CURSO\GitHUB\PRACTICA_RPA\DatosMeteorologicos.docx'
    pyperclip.copy(ruta_completa)  # Copia la ruta al portapapeles
    pyautogui.hotkey('ctrl', 'v')  # Pega la ruta en el cuadro de diálogo de guardado
    time.sleep(1)
    pyautogui.press('enter')  # Confirma el guardado
    time.sleep(2)  # Espera a que el documento se guarde
    # Mostrar mensaje de finalización por pantalla
    pyautogui.alert("Datos guardados correctamente.")

# Mostrar la alerta y pedir al usuario que ingrese una fecha
fecha_elegida = pyautogui.prompt("Por favor, ingrese una fecha en el formato 'AAAA-MM-DD' para la consulta:")

# Verificar si se ingresó una fecha
if fecha_elegida:
    try:
        # Intentar parsear la fecha para asegurarse de que tiene el formato correcto
        datetime.strptime(fecha_elegida, '%Y-%m-%d')
        
        # Configuración inicial con la fecha elegida
        clave_api = "_4MMKz3eDiSwUtRqqVi62W-a8XDVmoEgqa0o_bGC_o9vjOvROu"
        id_estacion = "TF164"
        fecha_inicial_str = fecha_elegida
        fecha_final_str = fecha_elegida  # La fecha final es la misma que la inicial
        
        # Construir la URL de la solicitud con la clave API y el ID de la estación
        url = f"https://servicio.mapama.gob.es/apisiar/API/v1/Datos/Horarios/Estacion?Id=TF164&FechaInicial={fecha_inicial_str}&FechaFinal={fecha_final_str}&ClaveAPI={clave_api}"
        
        # Realizar la solicitud
        respuesta = requests.get(url)
        
        # Verificar y procesar la respuesta
        if respuesta.status_code == 200:
            datos = respuesta.json()
            textos_para_word = []
            # Procesar y mostrar los datos solicitados
            for i, registro in enumerate(datos['Datos']):
                # Ajustar la fecha y hora para reflejar intervalos de 30 minutos
                fecha_hora_ajustada = datetime.strptime(registro['Fecha'], '%Y-%m-%dT%H:%M:%S')
                fecha_hora_ajustada += timedelta(minutes=30 * i)  # Incrementa 30 minutos por cada registro
                
                # Formatear la fecha ajustada para la impresión
                fecha_hora_str = fecha_hora_ajustada.strftime('%Y-%m-%d %H:%M:%S')
                
                linea = f"Fecha: {fecha_hora_str}, Radiación: {registro.get('Radiacion', 'No Disponible')}, Temp. Media: {registro.get('TempMedia', 'No Disponible')}°C, Vel. Viento: {registro.get('VelViento', 'No Disponible')} m/s, Dir. Viento: {registro.get('DirViento', 'No Disponible')}°"
                textos_para_word.append(linea)
            escribir_en_word(textos_para_word)
        else:
            print(f"Error al realizar la solicitud: {respuesta.status_code}, Detalles: {respuesta.text}")
    except ValueError:
        pyautogui.alert("El formato de la fecha no es correcto. Por favor, intente de nuevo usando el formato 'AAAA-MM-DD'.")
else:
    pyautogui.alert("No se ingresó ninguna fecha.")




