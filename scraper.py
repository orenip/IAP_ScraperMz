import os
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import time

# Cargar el archivo .env
load_dotenv()

# Función para esperar un elemento en la página
def esperar_elemento(driver, by, value, timeout=10):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))

# Función para esperar que un elemento sea clickeable
def esperar_elemento_clickeable(driver, by, value, timeout=10):
    return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, value)))

# Función para mostrar el tiempo restante
def mostrar_tiempo_restante(tiempo_restante):
    horas = tiempo_restante // 3600
    minutos = (tiempo_restante % 3600) // 60
    segundos = tiempo_restante % 60
    print(f"Tiempo restante hasta la próxima ejecución: {horas:02d}h {minutos:02d}m {segundos:02d}s", end="\r")

def ejecutar_scraper(usuario, contrasena, url):
    try:
        print("Intentando ejecutar en Windows...")

        # Configuración para Windows
        options = Options()
        #options.add_argument("--headless")  # Modo sin interfaz gráfica

        # No es necesario especificar la ruta de Firefox en Windows
        driver = webdriver.Firefox(
            service=Service(GeckoDriverManager().install()),  # Instala GeckoDriver automáticamente
            options=options
        )
    except Exception as e:
        print("Error al ejecutar", e)
        return
    
    if driver:  # Solo ejecutar si driver fue creado exitosamente
        try:
            driver.get(url)

            # Al entrar, hacer clic en el botón de cookies si existe
            try:
                cookie_button = esperar_elemento_clickeable(driver, By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")
                cookie_button.click()
            except:
                print("No se encontró el botón de cookies")

            # Login
            username_input = esperar_elemento(driver, By.ID, "login_username")
            password_input = esperar_elemento(driver, By.ID, "login_password")
            username_input.send_keys(usuario)
            password_input.send_keys(contrasena)
            next_button = esperar_elemento_clickeable(driver, By.ID, "login")
            next_button.click()

            # Esperar que la página cargue después de login
            esperar_elemento(driver, By.CLASS_NAME, "offer")

            # Clic en el primer evento
            event_button = esperar_elemento_clickeable(driver, By.CLASS_NAME, "offer")
            event_button.click()

            # Reclamar recompensa
            claim_button = esperar_elemento_clickeable(driver, By.ID, "claim")
            claim_button.click()

            # Imprimir primera recompensa obtenida
            print("Primera recompensa obtenida")

            # Cambiar deporte
            try:
                # Intentar 'Juega con tu equipo de hockey'
                hockey_link = esperar_elemento_clickeable(driver, By.XPATH, "//a[@href='/?p=clubhouse&changesport=hockey']")
                hockey_link.click()
                print("Clic en 'Juega con tu equipo de hockey'")

            except Exception as e:
                print("No se encontró el enlace de hockey, probando fútbol:", e)
                try:
                    # Si hockey falla, intentar con 'Juega con tu equipo de fútbol'
                    soccer_link = esperar_elemento_clickeable(driver, By.XPATH, "//a[@href='/?p=clubhouse&changesport=soccer']")
                    soccer_link.click()
                    print("Clic en 'Juega con tu equipo de fútbol'")
                except Exception as e:
                    print("No se encontró el enlace de fútbol tampoco:", e)

            try:
                # Esperar que el evento esté disponible para el deporte seleccionado
                esperar_elemento(driver, By.CLASS_NAME, "offer")

                # Clic en el segundo evento
                event_button = esperar_elemento_clickeable(driver, By.CLASS_NAME, "offer")
                event_button.click()

                # Reclamar segunda recompensa
                claim_button = esperar_elemento_clickeable(driver, By.ID, "claim")
                claim_button.click()

                # Imprimir segunda recompensa obtenida
                print("Segunda recompensa obtenida")

            except Exception as e:
                print(f"Error al intentar hacer clic en el segundo evento o reclamar la segunda recompensa: {e}")
            
        finally:
            if driver:
                driver.quit()
                print("Recompensas obtenidas exitosamente")

# --- Bucle principal ---
if __name__ == "__main__":
    usuario = os.getenv("USUARIO")
    contrasena = os.getenv("CONTRASENA")
    url = os.getenv("URL")
    
    intervalo_ejecucion = 14400  # 4 horas en segundos
    
    while True:
        try:
            # Ejecutar el scraper
            ejecutar_scraper(usuario, contrasena, url)
            
            # Contador de tiempo hasta la próxima ejecución
            tiempo_restante = intervalo_ejecucion
            while tiempo_restante > 0:
                mostrar_tiempo_restante(tiempo_restante)
                time.sleep(1)
                tiempo_restante -= 1
            
        except KeyboardInterrupt:
            print("\nPrograma detenido.")
            break
