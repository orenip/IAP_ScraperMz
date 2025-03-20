import time
import subprocess
import os
from dotenv import load_dotenv  # Importa load_dotenv

# Cargar las variables del archivo .env
load_dotenv()

def ejecutar_scraper():
    """Función para ejecutar el scraper"""
    print("Ejecutando Scraper.")
    # Ruta absoluta del archivo scraper.py
    script_path = os.getenv("RUTA")
    result = subprocess.run(['python', script_path], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("Scraper ejecutado con éxito.")
    else:
        print(f"Error al ejecutar el scraper: {result.stderr}")

def mostrar_tiempo_restante(segundos_restantes):
    """Función para mostrar el tiempo restante en una sola línea"""
    horas = segundos_restantes // 3600
    minutos = (segundos_restantes % 3600) // 60
    segundos = segundos_restantes % 60
    print(f"\rTiempo restante hasta la próxima ejecución: {horas} horas, {minutos} minutos, {segundos} segundos", end='', flush=True)

if __name__ == "__main__":
    intervalo_ejecucion = 14400  # 4 horas en segundos
    
    while True:
        try:
            # Ejecutar el scraper
            ejecutar_scraper()
            
            # Contar hacia atrás el tiempo restante hasta la siguiente ejecución
            tiempo_restante = intervalo_ejecucion
            while tiempo_restante > 0:
                mostrar_tiempo_restante(tiempo_restante)
                time.sleep(1)  # Esperar un segundo
                tiempo_restante -= 1  # Reducir 1 segundo
                
        except KeyboardInterrupt:
            print("\nPrograma detenido.")
            break
