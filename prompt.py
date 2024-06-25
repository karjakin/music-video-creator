def create_animation_structure(total_frames, interval, initial_state_a, initial_state_b, transitions_a, transitions_b):
    """
    Genera una estructura de animación con estados cambiantes en intervalos regulares.
    
    :param total_frames: Número total de frames en la animación.
    :param interval: Intervalo de frames para cada transición.
    :param initial_state_a: Estado inicial para pw_a.
    :param initial_state_b: Estado inicial para pw_b.
    :param transitions_a: Lista de transiciones para pw_a.
    :param transitions_b: Lista cíclica de transiciones para pw_b.
    :return: Diccionario con los frames como claves y los estados como valores.
    """
    animation_structure = {}
    num_intervals = total_frames // interval

    for i in range(num_intervals + 1):
        frame = i * interval
        if i == 0:
            state_a = initial_state_a
            state_b = initial_state_b
        elif i == num_intervals:
            state_a = transitions_a[-1]  # El último estado de pw_a
            state_b = transitions_b[i % len(transitions_b)]
        else:
            state_a = 'peak'
            state_b = transitions_b[i % len(transitions_b)]

        animation_structure[frame] = f"({state_a}:`pw_a`),({state_b}:`pw_b`)"

    return animation_structure

def distribute_prompts(animation_structure, prompts):
    """
    Añade prompts de una lista a una estructura de animación existente de manera uniforme, manteniendo el formato correcto de comillas.

    :param animation_structure: La estructura de animación existente.
    :param prompts: Lista de prompts para distribuir.
    :return: Lista de strings con el formato específico.
    """
    frames = list(animation_structure.keys())
    formatted_output = []
    for i, frame in enumerate(frames):
        formatted_output.append(f'"{frame}": "{animation_structure[frame]}, {prompts[i % len(prompts)]}"')
    return formatted_output

# Ejemplo de uso
total_frames = 440
interval = 40
initial_state_a = "begin"
initial_state_b = "silent"
transitions_a = ["grow", "peak", "fade", "diminish", "end"]
transitions_b = ["sparkle", "glisten", "twinkle", "quiet", "silent"]
prompt1="prompt"

prompts = [prompt1]

animation_structure = create_animation_structure(total_frames, interval, initial_state_a, initial_state_b, transitions_a, transitions_b)
print(len(animation_structure))
print(animation_structure)


updated_structure = distribute_prompts(animation_structure, prompts)



def convert_to_single_string(updated_structure):
   
    sorted_structure = sorted(updated_structure, key=lambda x: int(x.split('"')[1]))
    single_string = ",\n".join(sorted_structure)
    single_string = single_string.replace('"\'', '"')
    return single_string

# Ejemplo de uso
#single_string_output = convert_to_single_string(updated_structure )
#print(single_string_output)
