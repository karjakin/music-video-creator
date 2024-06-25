import pyautogui
import time
import os
import math
import sys
import random
sys.path.append("..")
from Ollamaprompt import stream_gen
from whisperr import song_to_video,song_to_video_intermedio
from random_styles import generate_musical_style


def click_closest_image(image_path, max_attempts=3):
    try:
        # Obtener la posición actual del cursor
        current_mouse_x, current_mouse_y = pyautogui.position()

        # Encontrar todas las instancias de la imagen en la pantalla
        locations = list(pyautogui.locateAllOnScreen(image_path))
        if not locations:
            print("No se encontró la imagen.")
            return False

        # Calcular cuál está más cerca del cursor actual
        closest_location = None
        min_distance = float('inf')
        for loc in locations:
            center_x, center_y = pyautogui.center(loc)
            distance = math.sqrt((center_x - current_mouse_x) ** 2 + (center_y - current_mouse_y) ** 2)
            if distance < min_distance:
                min_distance = distance
                closest_location = (center_x, center_y)

        # Intentar hacer clic en la ubicación más cercana
        attempts = 0
        while attempts < max_attempts:
            pyautogui.click(closest_location)
            # Aquí podrías añadir una verificación para confirmar si el clic fue exitoso
            print(f"Clic realizado en {closest_location}")
            attempts += 1
            return True

    except pyautogui.ImageNotFoundException:
        print("La imagen no fue encontrada en la pantalla.")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def obtener_archivo_mas_reciente(carpeta):
    # Obtener todos los archivos y carpetas en la ruta especificada
    elementos = os.listdir(carpeta)
    
    # Obtener las rutas completas
    rutas_completas = [os.path.join(carpeta, elemento) for elemento in elementos]
    
    # Filtrar solo aquellos que son archivos y no carpetas
    archivos = [ruta for ruta in rutas_completas if os.path.isfile(ruta)]
    
    # Si no hay archivos, retornar None
    if not archivos:
        return None
    
    # Obtener el archivo más reciente
    archivo_mas_reciente = max(archivos, key=os.path.getmtime)
    
    # Retornar solo el nombre del archivo más reciente
    return os.path.basename(archivo_mas_reciente)

# Ejemplo de uso


def abrir_navegador(busqueda):
    pyautogui.hotkey("win","r")
    pyautogui.write(f'chrome.exe "{busqueda}"')
    pyautogui.press("enter")
    time.sleep(3)

def click_img(img, confidence=0.9):
    try:
        time.sleep(1)
        x, y = pyautogui.locateCenterOnScreen(img, confidence=confidence)
        pyautogui.moveTo(x, y)
        pyautogui.click()
        time.sleep(1)
    except Exception as e:
        print(f"Ocurrió un error: {e}")

def click_img_error(img, confidence=0.9):

    time.sleep(1)
    x, y = pyautogui.locateCenterOnScreen(img, confidence=confidence)
    pyautogui.moveTo(x, y)
    pyautogui.click()
    time.sleep(1)



def go_img(img, confidence=0.9):
    try:
        time.sleep(1)
        x, y = pyautogui.locateCenterOnScreen(img, confidence=confidence)
        pyautogui.moveTo(x, y)
        time.sleep(1)
    except Exception as e:
        print(f"Ocurrió un error: {e}")

def click_img_interval(img,n):
    try:

        time.sleep(1)
        x, y = pyautogui.locateCenterOnScreen(img, confidence=0.8)
        pyautogui.moveTo(x, y)
        pyautogui.mouseDown(button='left')
        time.sleep(n)
        pyautogui.mouseUp( button='left')
        time.sleep(1)
            
    except Exception as e:
        print(f"Ocurrió un error: {e}")




def download_song():
    abrir_navegador("https://suno.com/create")
    time.sleep(1)
    click_img_interval("bajar.png",2)
    go_img("cancion_final.png")
    click_closest_image('puntos.png')
    click_img_error("download.png")
    click_img_error("audio.png")
    time.sleep(1)
    pyautogui.hotkey("ctrl","w")
    ruta_carpeta = r'C:\Users\jairc\Downloads'
    nombre_archivo_reciente = obtener_archivo_mas_reciente(ruta_carpeta)
    ruta_completa = f"{ruta_carpeta}\\{nombre_archivo_reciente}"
    print("El archivo más reciente es:", ruta_completa)

    return ruta_completa

def crear_cancion(style=""):
    max_attempts = 5
    attempt = 1
    start_time = time.time()
    print(start_time)

    while attempt <= max_attempts:
        try:
            output = stream_gen(style)
            print(output)
            abrir_navegador("https://suno.com/create")
            time.sleep(3)
            print("aqui?")
            click_img_error("inputprompt.png", 0.5)
            pyautogui.click()
            pyautogui.click()
            pyautogui.press('backspace')
            print("aca")
            pyautogui.write(output)
            click_img_error("create.png")
            time.sleep(120)
            ruta_cancion = download_song()
            return ruta_cancion
        except Exception as e:
            print(f"Intento {attempt} fallido: {e}")
            attempt += 1

            elapsed_time = time.time() - start_time
            if elapsed_time < 600:
                remaining_time = 600 - elapsed_time
                print(f"Esperando {remaining_time:.2f} segundos antes del siguiente intento.")
                time.sleep(remaining_time)
            else:
                print("Se alcanzó el tiempo máximo de espera.")
                break

    print("Se alcanzó el número máximo de intentos.")
    return None
if __name__=="__main__":

    while True:
        adjective=["psytrance","Progressive rock","psychedelic rock"]
        phrase = "psytrance,Progressive rock,psychedelic rock"
        style=generate_musical_style()
        style2=f"{phrase},{style}"
        print("##########")
        print(style2)
        print("##########")
        song=crear_cancion(style2)
        vid=song_to_video_intermedio(song)
        print(vid)
        time.sleep(10) 
        print("##########")
        print("next")    
        print("##########")           



