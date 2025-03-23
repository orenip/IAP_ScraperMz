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
def esperar_elemento(driver, by, value, timeout=30):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))

# Función para esperar que un elemento sea clickeable
def esperar_elemento_clickeable(driver, by, value, timeout=30):
    return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, value)))

# Función para mostrar el tiempo restante
def mostrar_tiempo_restante(tiempo_restante):
    horas = tiempo_restante // 3600
    minutos = (tiempo_restante % 3600) // 60
    segundos = tiempo_restante % 60
    print(f"Tiempo restante hasta la próxima ejecución: {horas:02d}h {minutos:02d}m {segundos:02d}s", end="\r")

# Función para verificar si se hizo clic en "claim"
def verificar_recompensa(driver):
    try:
        # Verificar si el botón "claim" ya no está presente o si aparece un mensaje de éxito
        WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.ID, "claim")))
        print("Recompensa obtenida correctamente.")
        return True
    except Exception as e:
        print("No se pudo verificar la recompensa:", e)
        return False

# Función para hacer clic en "claim" usando JavaScript
def hacer_clic_claim_con_javascript(driver):
    try:
        # Ejecutar la función JavaScript directamente
        driver.execute_script("mzEvent.claim();")
        print("Clic en 'claim' realizado mediante JavaScript.")
        return True
    except Exception as e:
        print("Error al ejecutar JavaScript para 'claim':", e)
        return False

# Función para manejar la alerta "Something went wrong"
def manejar_alerta(driver):
    try:
        # Esperar a que aparezca la alerta
        alerta = WebDriverWait(driver, 5).until(EC.alert_is_present())
        print("Alerta detectada:", alerta.text)
        alerta.accept()  # Aceptar la alerta
        print("Alerta aceptada.")
        return True
    except Exception as e:
        print("No se detectó ninguna alerta:", e)
        return False

# Función para cambiar de deporte
def cambiar_deporte(driver, deporte):
    intentos = 3  # Número de intentos para cambiar de deporte
    for intento in range(intentos):
        try:
            # Buscar el enlace del deporte
            deporte_link = esperar_elemento(driver, By.XPATH, f"//a[contains(@href, 'changesport={deporte}')]")
            
            # Desplazar la página para que el elemento sea visible
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", deporte_link)
            time.sleep(2)  # Esperar un momento para que la página se ajuste

            # Hacer clic en el enlace usando JavaScript
            driver.execute_script("arguments[0].click();", deporte_link)
            print(f"Clic en 'Juega con tu equipo de {deporte}' realizado.")

            # Esperar a que la página se cargue completamente
            time.sleep(5)  # Esperar un momento para que la página cargue
            driver.refresh()  # Recargar la página para asegurarse de que esté en el estado correcto

            # Verificar si el cambio de deporte fue exitoso
            esperar_elemento(driver, By.CLASS_NAME, "offer")  # Esperar a que los eventos estén disponibles
            print(f"Cambio a {deporte} exitoso.")
            return True
        except Exception as e:
            print(f"Intento {intento + 1}: Error al cambiar a {deporte}:", e)
            time.sleep(5)  # Esperar antes de reintentar

    print(f"No se pudo cambiar a {deporte} después de varios intentos.")
    return False

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
        return
    
    if driver:  # Solo ejecutar si driver fue creado exitosamente
        try:
            driver.get(url)

            # Login
            try:
                username_input = esperar_elemento(driver, By.ID, "login_username")
                password_input = esperar_elemento(driver, By.ID, "login_password")
                username_input.send_keys(usuario)
                password_input.send_keys(contrasena)
                next_button = esperar_elemento_clickeable(driver, By.ID, "login")
                next_button.click()
                print("Login realizado correctamente.")
            except Exception as e:
                print("Error durante el login:", e)
                raise  # Relanzar la excepción para detener la ejecución

            # Esperar que la página cargue después de login
            try:
                esperar_elemento(driver, By.CLASS_NAME, "offer")
                print("Página cargada correctamente después del login.")
            except Exception as e:
                print("Error al cargar la página después del login:", e)
                raise

            # Clic en el primer evento
            try:
                event_button = esperar_elemento_clickeable(driver, By.CLASS_NAME, "offer")
                event_button.click()
                print("Clic en el primer evento realizado.")
            except Exception as e:
                print("Error al hacer clic en el primer evento:", e)
                raise

            # Reclamar recompensa con reintentos
            intentos = 5  # Aumentamos el número de intentos
            recompensa_obtenida = False
            for intento in range(intentos):
                try:
                    # Verificar si el botón está habilitado
                    claim_button = esperar_elemento(driver, By.ID, "claim")
                    if "buttondiv_disabled" not in claim_button.get_attribute("class"):
                        claim_button.click()
                        print(f"Intento {intento + 1}: Clic en 'claim' realizado.")
                    else:
                        print(f"Intento {intento + 1}: El botón 'claim' está deshabilitado.")
                        # Intentar hacer clic usando JavaScript
                        if hacer_clic_claim_con_javascript(driver):
                            recompensa_obtenida = True
                            break

                    # Esperar y verificar si la recompensa se obtuvo
                    time.sleep(5)  # Esperar un momento para que la página actualice
                    if verificar_recompensa(driver):
                        recompensa_obtenida = True
                        break  # Salir del bucle si la recompensa se obtuvo
                except Exception as e:
                    print(f"Intento {intento + 1}: Error al hacer clic en 'claim':", e)
                    time.sleep(5)  # Esperar antes de reintentar

            if not recompensa_obtenida:
                print("No se ha obtenido recompensa después de varios intentos.")

            # Cambiar deporte a hockey
            if not cambiar_deporte(driver, "hockey"):
                print("No se pudo cambiar a hockey. Probando fútbol...")
                if not cambiar_deporte(driver, "soccer"):
                    print("No se pudo cambiar a fútbol tampoco.")

            # Reclamar segunda recompensa con reintentos
            intentos = 5  # Aumentamos el número de intentos
            recompensa_obtenida = False
            for intento in range(intentos):
                try:
                    # Esperar que el evento esté disponible para el deporte seleccionado
                    esperar_elemento(driver, By.CLASS_NAME, "offer")

                    # Clic en el segundo evento
                    event_button = esperar_elemento_clickeable(driver, By.CLASS_NAME, "offer")
                    event_button.click()

                    # Reclamar segunda recompensa
                    claim_button = esperar_elemento(driver, By.ID, "claim")
                    if "buttondiv_disabled" not in claim_button.get_attribute("class"):
                        claim_button.click()
                        print(f"Intento {intento + 1}: Clic en 'claim' realizado.")
                    else:
                        print(f"Intento {intento + 1}: El botón 'claim' está deshabilitado.")
                        # Intentar hacer clic usando JavaScript
                        if hacer_clic_claim_con_javascript(driver):
                            recompensa_obtenida = True
                            break

                    # Esperar y verificar si la recompensa se obtuvo
                    time.sleep(5)  # Esperar un momento para que la página actualice
                    if verificar_recompensa(driver):
                        recompensa_obtenida = True
                        break  # Salir del bucle si la recompensa se obtuvo
                except Exception as e:
                    print(f"Intento {intento + 1}: Error al hacer clic en 'claim':", e)
                    time.sleep(5)  # Esperar antes de reintentar

            if not recompensa_obtenida:
                print("No se ha obtenido la segunda recompensa después de varios intentos.")

        except Exception as e:
            print(f"Error durante el scraping: {e}")
        
        finally:
            if driver:
                # Esperar antes de cerrar el navegador
                time.sleep(10)  # Esperar 10 segundos antes de cerrar
                driver.quit()
                print("Navegador cerrado.")

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