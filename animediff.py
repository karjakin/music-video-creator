
from urllib import request, error
import json
import random
import os
import time

def listar_elementos(ruta):
    elementos = []

    if os.path.exists(ruta):
        for elemento in os.listdir(ruta):
            ruta_completa = os.path.join(ruta, elemento)
            elementos.append(ruta_completa)
    else:
        print(f"La ruta '{ruta}' no existe.")

    return elementos

def monitor_directory(path, threshold, json_output_path):
    while True:
        try:
            # Lista todos los archivos en el directorio
            file_list = os.listdir(path)
            # Cuenta la cantidad de archivos
            file_count = len(file_list)

            print(f"Comprobando... {file_count} archivos encontrados.")  # Imprime la cantidad de archivos actual

            # Si se alcanza o supera el umbral, crea un archivo JSON
            if file_count >= threshold:
                image_data = {f"{i}": os.path.join(path, file) for i, file in enumerate(file_list, start=1)}
                with open(json_output_path, 'w') as json_file:
                    json.dump(image_data, json_file, indent=4)
                
                print(f"Archivo JSON creado con {file_count} elementos.")
                return image_data # Termina el bucle después de crear el archivo JSON
            else:
                print(f"Esperando a alcanzar el umbral de {threshold} archivos...")

            # Espera 10 segundos antes de la próxima comprobación
            time.sleep(20)
        except Exception as e:
            print(f"Error: {e}")
            break


json_file_path2 = 'animediff_upscaler3.json'

with open(json_file_path2, 'r', encoding='utf-8') as json_file:
    data2 = json.load(json_file)



def queue_prompt(prompt):
    try:
        p = {"prompt": prompt}
        data = json.dumps(p).encode('utf-8')  # Convert the Python dictionary back to a JSON formatted string to send in the request
        req = request.Request("http://127.0.0.1:8188/prompt", data=data)
        with request.urlopen(req) as response:
            print("Request successful, response:", response.read())
    except error.HTTPError as e:
        print('HTTPError: ', e.code, e.reason)
    except error.URLError as e:
        print('URLError: ', e.reason)
    except Exception as e:
        print('Generic Exception: ', e)



def animediff_upscaler(img_path,prompt, id, neg_prompts,directory_path):
    print(prompt)
    print(neg_prompts)
    print(img_path)
   
    # Create directory
    dir_path = directory_path
    os.makedirs(dir_path, exist_ok=True)
    print(f"Directory created at {dir_path}")
    data2["66"]["inputs"]["strength"] = 0.9
    data2["66"]["inputs"]["end_percent"] = 0.35
    data2["64"]["inputs"]["positive"]="high detail, hd , intricate"
    data2["130"]["inputs"]["video"] = img_path
    data2["91"]["inputs"]["filename_prefix"] = f"steerable-motion_{id}/final_AD_"
    queue_prompt(data2)  # Assuming this generates the image and saves it to the specified path

   
def call_animediff_upscaler(img_path,prompt, id, neg_prompts,directory_path,limite):
    json_output_path = "output3.json"
    animediff_upscaler(img_path,prompt, id, neg_prompts,directory_path)    
    output=monitor_directory(directory_path,limite,json_output_path)
    print(output)
    return output



def list_dir_contents(dir_path):
    dir_contents = []
    
    try:
        # Obtener una lista de los elementos dentro del directorio
        elements = os.listdir(dir_path)
        
        # Agregar cada elemento a la lista de contenidos
        for element in elements:
            element_path = os.path.join(dir_path, element)
            dir_contents.append(element_path)
        
        return dir_contents
    
    except FileNotFoundError:
        print(f"El directorio '{dir_path}' no existe.")
        return []
    
    except PermissionError:
        print(f"No tienes permisos para acceder al directorio '{dir_path}'.")
        return []
    
def replace_text(text, substring, replacement):
    if substring in text:
        return text.replace(substring, replacement)
    else:
        return text
if __name__ == "__main__" :
  
    prompt=""
    
    neg_prompts= "text"
    
    folder=r"C:\\Users\\jairc\\Downloads\\videos"
    paths=listar_elementos(folder)
    limite= 2
    print(paths)

    for path in paths:
        def generate_random_15_digit_number():
            return random.randint(100000000000000, 999999999999999)

        id=generate_random_15_digit_number()
        directory_path = f"C:\\Users\\jairc\\Pictures\\comfyui face\\ComfyUI\\output\\steerable-motion_{id}"
        video_upscaler=call_animediff_upscaler(path,prompt, id, neg_prompts,directory_path,limite)
        print(video_upscaler)



    
