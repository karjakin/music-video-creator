from pydub import AudioSegment

def calcular_frames(archivo_audio):
    # Cargar el archivo de audio
    audio = AudioSegment.from_file(archivo_audio)
    
    # Obtener la duración del audio en milisegundos
    duracion_ms = len(audio)
    
    # Calcular la duración del audio en segundos
    duracion_s = duracion_ms / 1000
    
    # Obtener la tasa de muestreo del audio
    tasa_muestreo = audio.frame_rate
    
    # Calcular la cantidad de frames para 12 segundos
    frames_12_segundos = int(tasa_muestreo * 12)
    
    # Verificar si el audio tiene una duración menor a 12 segundos
    if duracion_s < 12:
        # Si la duración es menor a 12 segundos, calcular los frames para la duración real
        frames = int(tasa_muestreo * duracion_s)
    else:
        # Si la duración es mayor o igual a 12 segundos, usar los frames para 12 segundos
        frames = frames_12_segundos
    
    return frames
def generar_prompt(cantidad_frames, distancia_prompts):
    pasos = [
        '"(begin:\"pw_a\"),(silent:\"pw_b\")"',
        '"(grow:\"pw_a\"),(sparkle:\"pw_b\")"',
        '"(peak:\"pw_a\"),(shimmer:\"pw_b\")"',
        '"(peak:\"pw_a\"),(glisten:\"pw_b\")"',
        '"(peak:\"pw_a\"),(twinkle:\"pw_b\")"',
        '"(peak:\"pw_a\"),(quiet:\"pw_b\")"',
        '"(peak:\"pw_a\"),(silent:\"pw_b\")"',
        '"(peak:\"pw_a\"),(sparkle:\"pw_b\")"',
        '"(peak:\"pw_a\"),(shimmer:\"pw_b\")"',
        '"(fade:\"pw_a\"),(glisten:\"pw_b\")"',
        '"(diminish:\"pw_a\"),(twinkle:\"pw_b\")"',
        '"(end:\"pw_a\"),(quiet:\"pw_b\")"'
    ]

    prompt = {}
    frame_actual = 0
    paso_actual = 0

    while frame_actual <= cantidad_frames:
        if paso_actual < len(pasos):
            prompt[str(frame_actual)] = pasos[paso_actual]
            paso_actual += 1
        else:
            prompt[str(frame_actual)] = '"(peak:\"pw_a\"),(shimmer:\"pw_b\")"'
            paso_intermedio = 1
            frame_intermedio = frame_actual + distancia_prompts

            while frame_intermedio <= cantidad_frames:
                if paso_intermedio == 1:
                    prompt[str(frame_intermedio)] = '"(peak:\"pw_a\"),(glisten:\"pw_b\")"'
                elif paso_intermedio == 2:
                    prompt[str(frame_intermedio)] = '"(peak:\"pw_a\"),(twinkle:\"pw_b\")"'
                elif paso_intermedio == 3:
                    prompt[str(frame_intermedio)] = '"(peak:\"pw_a\"),(quiet:\"pw_b\")"'
                elif paso_intermedio == 4:
                    prompt[str(frame_intermedio)] = '"(peak:\"pw_a\"),(silent:\"pw_b\")"'
                elif paso_intermedio == 5:
                    prompt[str(frame_intermedio)] = '"(peak:\"pw_a\"),(sparkle:\"pw_b\")"'
                else:
                    prompt[str(frame_intermedio)] = '"(peak:\"pw_a\"),(shimmer:\"pw_b\")"'
                    paso_intermedio = 0

                paso_intermedio += 1
                frame_intermedio += distancia_prompts

        frame_actual += distancia_prompts

    return prompt

archivo_audio = r"C:\Users\jairc\Downloads\Natanael-Cano_-Bzrp-Music-Sessions_-Vol.-59-_152kbit_Opus_.mp3"
frames = calcular_frames(archivo_audio)
distancia_prompts=1000
prompt_generado = generar_prompt(frames, distancia_prompts)
print(prompt_generado)
print("Cantidad de frames en 12 segundos:", frames)