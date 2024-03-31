from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import glob

download_folder = "C:\\Users\\angel\\Desktop\\MASTER\\TFM"

options = webdriver.ChromeOptions()  # Opciones de navegación con selenium
options.add_argument("--headless")  # Comentar esta línea si se desea ver la ejecución en modo no headless
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920x1080")
prefs = {
    "download.default_directory": download_folder,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True,
    "safebrowsing.disable_download_protection": True,
    "profile.default_content_setting_values.automatic_downloads": 1,
}
options.add_experimental_option("prefs", prefs)
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Función para esperar la descarga completa del archivo y guardarlo como el archivo más reciente
def esperar_descarga_completa(extension="xls", timeout=60):
    start_time = time.time()
    while True:
        files = glob.glob(download_folder + f"/*.{extension}")
        if files:
            latest_file = max(files, key=os.path.getctime)  # Obtener el archivo más reciente
            print("Archivo descargado con éxito: " + latest_file)
            print()
            return latest_file
        elif time.time() - start_time > timeout:
            print("Tiempo de espera para la descarga excedido.")
            print()
            return None
        time.sleep(1)
        
# Inicio de sesión y descarga de datos de Sems Portal para los últimos 351 días
login_url = "https://www.semsportal.com/home/login"
driver.get(login_url)

# Completar el formulario de inicio de sesión
time.sleep(2)  # Esperar a que la página cargue

# Esperar a que la página cargue y localizar la casilla de condiciones de uso y política de privacidad
checkbox = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "readStatement"))
)

# Hacer clic en la casilla de verificación si no está ya seleccionada
if not checkbox.is_selected():
    checkbox.click()
    
email_input = driver.find_element(By.ID, "username")
password_input = driver.find_element(By.ID, "password")
login_button = driver.find_element(By.ID, "btnLogin")

# Credenciales
your_email = "alu0101214559@ull.edu.es"
your_password = "Goodwe2018"

email_input.send_keys(your_email)
password_input.send_keys(your_password)
login_button.click()

time.sleep(5)  # Esperar a que la página cargue

# Localizar el elemento por el texto que contiene
plant_link = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'SEGAI - ULL')]"))
)
plant_link.click()

# Esperar a que la página cargue después del inicio de sesión
time.sleep(5)  # Espera para que todos los elementos se carguen completamente

# Navegar a la URL específica
driver.get("https://www.semsportal.com/powerstation/PowerStatusSnMin/2c6eb65e-dca9-4c6f-810f-769064cc6ca8")

# No se retrocede un día antes de la primera descarga
for day in range(370):  # Incluye el día actual y los 350 días anteriores
    max_retries = 3
    archivo_descargado = False  # Indica si el archivo ha sido descargado correctamente

    for attempt in range(max_retries):
        try:
            WebDriverWait(driver, 20).until(EC.invisibility_of_element((By.CSS_SELECTOR, '.el-loading-mask')))
            WebDriverWait(driver, 20).until(EC.invisibility_of_element((By.CSS_SELECTOR, '.el-loading-spinner')))
            
            action = ActionChains(driver)
            export_icon = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".goodwe-station-charts__export.fr"))
            )
            action.move_to_element(export_icon).click().perform()

            archivo_reciente = esperar_descarga_completa(extension="xls")
            if archivo_reciente:
                print(f"Clic en el icono de exportación realizado con éxito y archivo descargado para el día actual o el día {day} en retrospectiva.")
                print()
                archivo_descargado = True
                break  # Sale del bucle de reintentos si se descarga el archivo con éxito
            else:
                print(f"Intento {attempt + 1} de descarga fallido. Reintentando...")
                print()
        except Exception as e:
            print(f"Ocurrió un error durante el intento {attempt + 1}: {e}")
            print()

        time.sleep(5)  # Espera antes de reintentar

    # Si el archivo se descargó correctamente o después del primer día, procede a retroceder un día para la siguiente iteración
    if day != 0 and archivo_descargado:  # Se añade la comprobación de archivo_descargado para asegurar que solo retrocedemos si el día actual fue exitoso
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".station-date-picker_left"))).click()
        time.sleep(2)  # Espera a que la página se actualice

# Cerrar el navegador al finalizar todas las descargas
driver.quit()
