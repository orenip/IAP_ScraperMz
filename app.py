import time
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import getpass

# --- Función para crear el .env si no existe ---
def crear_env():
    print("Configuración inicial: Por favor ingresa los siguientes datos.")
    usuario = input("Usuario de MZ: ")
    contrasena = getpass.getpass("Contraseña de MZ: ")  # Ocultar la contraseña
    url = input("URL de MZ (default: https://www.managerzone.com/): ") or "https://www.managerzone.com/"
    
    with open(".env", "w") as env_file:
        env_file.write(f"USUARIO={usuario}\n")
        env_file.write(f"CONTRASENA={contrasena}\n")
        env_file.write(f"URL={url}\n")
    
    print("Configuración guardada en .env. Continuando...")

# --- Cargar el archivo .env ---
if not os.path.exists(".env"):
    crear_env()

load_dotenv()

# --- Scraper integrado ---
def ejecutar_scraper(usuario, contrasena, url):
    try:
        print("Iniciando navegador en modo headless...")
        options = Options()
        options.add_argument("--headless")

        driver = webdriver.Firefox(
            service=Service(GeckoDriverManager().install()),
            options=options
        )

        driver.get(url)

        # Intentar aceptar cookies si existe el botón
        try:
            cookie_button = driver.find_element(By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")
            cookie_button.click()
        except:
            print("No se encontró el botón de cookies")

        # Ingreso de usuario y contraseña
        username_input = driver.find_element(By.ID, "login_username")
        password_input = driver.find_element(By.ID, "login_password")

        username_input.send_keys(usuario)
        password_input.send_keys(contrasena)

        next_button = driver.find_element(By.ID, "login")
        next_button.click()

        time.sleep(10)

        # Recolectar primera recompensa
        event_button = driver.find_element(By.CLASS_NAME, "offer")
        event_button.click()
        time.sleep(5)
        claim_button = driver.find_element(By.ID, "claim")
        claim_button.click()
        print("Primera recompensa obtenida")

        # Cambiar a equipo de hockey
        try:
            hockey_link = driver.find_element(By.XPATH, "//a[@href='/?p=clubhouse&changesport=hockey']")
            hockey_link.click()
            print("Clic en 'Juega con tu equipo de hockey'")
        except Exception as e:
            print("No se encontró el enlace de hockey:", e)

        time.sleep(5)

        # Cambiar a equipo de fútbol
        try:
            soccer_link = driver.find_element(By.XPATH, "//a[@href='/?p=clubhouse&changesport=soccer']")
            soccer_link.click()
            print("Clic en 'Juega con tu equipo de fútbol'")
        except Exception as e:
            print("No se encontró el enlace de fútbol:", e)

        time.sleep(5)

        # Recolectar segunda recompensa
        event_button = driver.find_element(By.CLASS_NAME, "offer")
        event_button.click()
        time.sleep(5)
        claim_button = driver.find_element(By.ID, "claim")
        claim_button.click()
        print("Segunda recompensa obtenida")

    except Exception as e:
        print(f"Error durante el scraping: {e}")
    
    finally:
        if driver:
            driver.quit()
            print("Recompensas obtenidas exitosamente")

# --- Control del tiempo de espera ---
def mostrar_tiempo_restante(segundos_restantes):
    horas = segundos_restantes // 3600
    minutos = (segundos_restantes % 3600) // 60
    segundos = segundos_restantes % 60
    print(f"\rTiempo restante hasta la próxima ejecución: {horas}h {minutos}m {segundos}s", end='', flush=True)

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
