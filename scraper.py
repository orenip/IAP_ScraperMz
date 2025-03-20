import os
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
import time
from dotenv import load_dotenv
from selenium.webdriver.firefox.options import Options

# Cargar el archivo .env
load_dotenv()

def ejecutar_scraper(usuario, contrasena, url):
    try:
        print("Intentando ejecutar en Windows...")

        # Configuración para Windows
        options = Options()
        options.add_argument("--headless")  # Modo sin interfaz gráfica

        # No es necesario especificar la ruta de Firefox en Windows
        driver = webdriver.Firefox(
            service=Service(GeckoDriverManager().install()),  # Instala GeckoDriver automáticamente
            options=options
        )
    except Exception as e:
                print("Error al ejecutar", e)
    
    
    # Resto del código sin cambios
    if driver:  # Solo ejecutar si driver fue creado exitosamente
        try:
            driver.get(url)
            # Al entrar, hacer clic en el botón id= CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll si existe
            try:
                cookie_button = driver.find_element(By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")
                cookie_button.click()
            except:
                print("No se encontró el botón de cookies")

            username_input = driver.find_element(By.ID, "login_username")
            password_input = driver.find_element(By.ID, "login_password")

            username_input.send_keys(usuario)
            password_input.send_keys(contrasena)

            next_button = driver.find_element(By.ID, "login")
            next_button.click()

            time.sleep(10)

            event_button = driver.find_element(By.CLASS_NAME, "offer")
            event_button.click()

            time.sleep(5)

            claim_button = driver.find_element(By.ID, "claim")
            claim_button.click()

            # Imprimir primera recompensa obtenida
            print("Primera recompensa obtenida")

            # Hacer clic en el enlace 'Juega con tu equipo de hockey'
            try:
                hockey_link = driver.find_element(By.XPATH, "//a[@href='/?p=clubhouse&changesport=hockey']")
                hockey_link.click()
                print("Clic en 'Juega con tu equipo de hockey'")
            except Exception as e:
                print("No se encontró el enlace de hockey:", e)

            time.sleep(5)

            # Hacer clic en el enlace 'Juega con tu equipo de fútbol'
            try:
                hockey_link = driver.find_element(By.XPATH, "//a[@href='/?p=clubhouse&changesport=soccer']")
                hockey_link.click()
                print("Clic en 'Juega con tu equipo de fútbol'")
            except Exception as e:
                print("No se encontró el enlace de futbol:", e)

            time.sleep(10)

            event_button = driver.find_element(By.CLASS_NAME, "offer")
            event_button.click()

            time.sleep(5)

            claim_button = driver.find_element(By.ID, "claim")
            claim_button.click()

            # Imprimir segunda recompensa obtenida
            print("Segunda recompensa obtenida")

            time.sleep(5)

        except Exception as e:
            print(f"Error durante el scraping: {e}")
        
        finally:
            if driver:
                driver.quit()
                print("Recompensas obtenidas exitosamente")

if __name__ == "__main__":
    usuario = os.getenv("USUARIO")
    contrasena = os.getenv("CONTRASENA")
    url = os.getenv("URL")
    ejecutar_scraper(usuario, contrasena, url)
