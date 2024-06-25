import whisper
from Ollamaprompt import stream_window,stream_intermedio
from pydub import AudioSegment
from music_video import generate_random_15_digit_number, call_animediff

def extract_segment_info(segments):
    # Lista para guardar la información extraída
    extracted_info = []
    
    # Iterar sobre cada segmento en la lista de segmentos
    for segment in segments:
        # Extraer 'start', 'end', y 'text' de cada segmento
        info = {
            'start': segment['start'],
            'end': segment['end'],
            'text': segment['text']
        }
        # Añadir el diccionario con la información extraída a la lista
        extracted_info.append(info)
    
    return extracted_info

def window_context(segments, num):
    # Initialize segments to empty strings for edge cases
    last_segment_text = ""
    new_segment_text = ""

    # Check and assign last segment if it exists
    if num - 1 >= 0:
        last_segment = segments[num - 1]
        last_segment_text = last_segment['text']

    # Check and assign next segment if it exists
    if num + 1 < len(segments):
        new_segment = segments[num + 1]
        new_segment_text = new_segment['text']

    # Current segment text
    segment = segments[num]
    segment_text = segment['text']

    # Create a window context by concatenating texts
    window = f"{last_segment_text}{segment_text}{new_segment_text}"
    return window

def add_window(segments):
    # Lista para guardar la información extraída
    extracted_info = []
    n = 0
    # Iterar sobre cada segmento en la lista de segmentos
    for segment in segments:
        window = window_context(segments, n)
        n = n + 1
        # Extraer 'start', 'end', y 'text' de cada segmento
        info = {
            'start': segment['start'],
            'end': segment['end'],
            'text': segment['text'],
            'window': window
        }
        # Añadir el diccionario con la información extraída a la lista
        extracted_info.append(info)
    
    return extracted_info

def transform_to_template_structure(win):
    frame_rate = 12  # frames per second
    
    # Define structure template based on provided information
    keywords = [
        ("begin", "silent"), ("peak", "glisten"), ("peak", "twinkle"), ("peak", "quiet"),
        ("peak", "silent"), ("peak", "sparkle"), ("peak", "glisten"), ("peak", "twinkle"),
        ("peak", "quiet"), ("peak", "silent"), ("peak", "sparkle"), ("end", "glisten")
    ]
    
    # Convert time from seconds to frames and map to keywords
    template_structure = {}
    keyword_index = 0
    for entry in win:
        start_frame = int(entry['start'] * frame_rate)
        end_frame = int(entry['end'] * frame_rate)
        window_text = entry['window']
        
        while keyword_index < len(keywords) and start_frame <= end_frame:
            if keyword_index < len(keywords):
                keyword_a, keyword_b = keywords[keyword_index]
                # Format the prompt according to the specified structure
                template_structure[str(start_frame)] = f"({keyword_a}:`{window_text}`),({keyword_b}:`{window_text}`), {entry['text']}"
                start_frame += 40  # assuming each segment represents a period in frames as defined in the structure
            keyword_index += 1
    
    return template_structure

def create_animation_structure(times, initial_state_a, initial_state_b, transitions_a, transitions_b):

    animation_structure = {}
    fps = 12  # Frames por segundo

    for i, time in enumerate(times):
        frame = int(time * fps)
        if i == 0:
            state_a = initial_state_a
            state_b = initial_state_b

        elif i == len(times)-1:
            state_a = transitions_a[-1]  # El último estado de pw_a
            state_b = transitions_b[i % len(transitions_b)]
        
        else:
            state_a = 'peak'
            state_b = transitions_b[(i-1) % len(transitions_b)]

        animation_structure[frame] = f"({state_a}:`pw_a`),({state_b}:`pw_b`)"

    return animation_structure

def distribute_prompts(animation_structure, prompts):

    frames = list(animation_structure.keys())
    formatted_output = []
    for i, frame in enumerate(frames):
        formatted_output.append(f'"{frame}": "{animation_structure[frame]}, {prompts[i % len(prompts)]}"')
    return formatted_output

def convert_to_single_string(updated_structure):
   
    sorted_structure = sorted(updated_structure, key=lambda x: int(x.split('"')[1]))
    single_string = ",\n".join(sorted_structure)
    single_string = single_string.replace('"\'', '"')
    return single_string


def calcular_f(archivo_audio):
    # Cargar el archivo de audio
    audio = AudioSegment.from_file(archivo_audio)
    
    # Obtener la duración del audio en milisegundos
    duracion_ms = len(audio)
    
    # Calcular la duración del audio en segundos
    duracion_s = duracion_ms / 1000

    frames=duracion_s*12
    
    
    return int(frames)

def call_whisper(song):
    model = whisper.load_model("medium")
    result = model.transcribe(song,language='en')
    print(result["segments"])
    extracted_segments = extract_segment_info(result["segments"])
    return extracted_segments


def call_window(extracted_segments):
    win=add_window(extracted_segments)
    for segment in win:
        #print(segment["window"])
        window=stream_window(segment["window"])
        print("--------")
        segment["prompt_window"] = window
    window_prompts=[]
    for dic in win:
        window_prompts.append(dic["prompt_window"].replace("\"","").replace("\n","").rstrip(", "))
    return window_prompts, win


def extract_time(song_lyrics):
    tiempos=[]
    for dic in song_lyrics:
        tiempos.append(dic["start"])
    return tiempos

#segments=[{'id': 0, 'seek': 0, 'start': 0.0, 'end': 9.0, 'text': ' Caminamos sin risa con el alma desnuda', 'tokens': [50364, 6886, 259, 2151, 3343, 2253, 64, 416, 806, 32634, 730, 77, 11152, 50814], 'temperature': 0.0, 'avg_logprob': -0.20623941006867783, 'compression_ratio': 1.26, 'no_speech_prob': 0.5180521011352539}, {'id': 1, 'seek': 0, 'start': 9.0, 'end': 15.0, 'text': ' Abrazando recuerdos en el viento se acunan', 'tokens': [50814, 2847, 30695, 1806, 39092, 33749, 465, 806, 371, 7814, 369, 696, 409, 282, 51114], 'temperature': 0.0, 'avg_logprob': -0.20623941006867783, 'compression_ratio': 1.26, 'no_speech_prob': 0.5180521011352539}, {'id': 2, 'seek': 0, 'start': 15.0, 'end': 22.0, 'text': ' Sin miedo al silencio, el silencio nos habla', 'tokens': [51114, 11187, 40383, 419, 3425, 268, 8529, 11, 806, 3425, 268, 8529, 3269, 42135, 51464], 'temperature': 0.0, 'avg_logprob': -0.20623941006867783, 'compression_ratio': 1.26, 'no_speech_prob': 0.5180521011352539}, {'id': 3, 'seek': 2200, 'start': 22.0, 'end': 30.0, 'text': ' Guitarras nos guían por caminos de plata y bajo la luna', 'tokens': [50364, 460, 1983, 2284, 296, 3269, 695, 11084, 1515, 1945, 15220, 368, 30780, 288, 30139, 635, 287, 5051, 50764], 'temperature': 0.0, 'avg_logprob': -0.12804502248764038, 'compression_ratio': 1.2444444444444445, 'no_speech_prob': 0.10511653125286102}, {'id': 4, 'seek': 2200, 'start': 35.0, 'end': 45.0, 'text': ' No buscamos luces que siguen por brillar y bajo la luna', 'tokens': [51014, 883, 1255, 66, 2151, 10438, 887, 631, 4556, 7801, 1515, 8695, 289, 288, 30139, 635, 287, 5051, 51514], 'temperature': 0.0, 'avg_logprob': -0.12804502248764038, 'compression_ratio': 1.2444444444444445, 'no_speech_prob': 0.10511653125286102}, {'id': 5, 'seek': 4500, 'start': 46.0, 'end': 53.0, 'text': ' Caminamos sin pesar', 'tokens': [50414, 6886, 259, 2151, 3343, 41951, 50764], 'temperature': 0.0, 'avg_logprob': -0.3434207153320312, 'compression_ratio': 1.0857142857142856, 'no_speech_prob': 0.10547828674316406}, {'id': 6, 'seek': 4500, 'start': 53.0, 'end': 65.0, 'text': ' No queremos glorias que solo sean fugaces y bajo la luna', 'tokens': [50764, 883, 26813, 1563, 284, 4609, 631, 6944, 37670, 31838, 2116, 288, 30139, 635, 287, 5051, 51364], 'temperature': 0.0, 'avg_logprob': -0.3434207153320312, 'compression_ratio': 1.0857142857142856, 'no_speech_prob': 0.10547828674316406}]
#extracted_segments = extract_segment_info(segments)
#for segment in extracted_segments:
#    print(segment)

def preproceso_prompt(song):
    song_lyrics=call_whisper(song)
    list_prompts,full_prompt=call_window(song_lyrics)
    print("full prompt")
    print(full_prompt)
    print("list prompt")
    print(list_prompts)
    time=extract_time(full_prompt)

    #win=[{'start': 0.0, 'end': 9.0, 'text': ' Caminamos sin risa con el alma desnuda', 'window': ' Caminamos sin risa con el alma desnuda Abrazando recuerdos en el viento se acunan', 'prompt_window': "Wistful wanderers traverse the windswept terrain, souls exposed like autumn leaves stripped of their vibrant hues, as they cling to memories carried on whispers of breeze. Golden light casts long shadows across the rust-red landscape, where ancient trees stand sentinel, their gnarled branches etched against a sky of softest blue. In the distance, a lone cypress rises like a dark, slender finger, reaching for the heavens as the wanderers' footsteps fade into the horizon's haze."}, {'start': 9.0, 'end': 15.0, 'text': ' Abrazando recuerdos en el viento se acunan', 'window': ' Caminamos sin risa con el alma desnuda Abrazando recuerdos en el viento se acunan Sin miedo al silencio, el silencio nos habla', 'prompt_window': "Two wanderers, their bare souls exposed to the elements, walk hand in hand along a worn dirt path, the wind carrying whispers of forgotten memories. The sky above is a soft blend of blue and gray, with wispy clouds scattered like cotton candy tufts. As they stroll, the silence between them is palpable, yet somehow comforting. In the distance, a lone tree stands sentinel, its branches etched against the sky like a delicate pen and ink drawing.\n\nTo the left, a hill rises, covered in a tapestry of golden grasses that seem to undulate in the breeze like a gentle wave. The air is filled with the sweet scent of blooming wildflowers, their colors muted to shades of lavender and peach. A few scattered stones dot the landscape, worn smooth by time and weather.\n\nThe camera pans down to reveal the wanderers' feet, bare and dusty, as they disappear into the distance, leaving behind only the faintest hint of a trail. The silence is almost audible, a palpable force that wraps around the scene like a gentle embrace."}, {'start': 15.0, 'end': 22.0, 'text': ' Sin miedo al silencio, el silencio nos habla', 'window': ' Abrazando recuerdos en el viento se acunan Sin miedo al silencio, el silencio nos habla Guitarras nos guían por caminos de plata y bajo la luna', 'prompt_window': 'Moonlit path unwinds like a silver ribbon, guitars echoing through the night air as memories settle softly with the wind. In this ethereal scene, silence is not oppressive, but rather a gentle companion that whispers secrets to those who listen. The camera pans down to reveal a lone traveler, a figure cloaked in misty shadows, following the melodic trail beneath the lunar glow. As they wander, the guitars lead them through an ever-changing landscape of moon-kissed hills and valleys, where stars twinkle like diamonds scattered across the velvet expanse. In the distance, a great tree stands sentinel, its branches etched against the sky like a delicate silver pen and ink drawing.'}, {'start': 22.0, 'end': 30.0, 'text': ' Guitarras nos guían por caminos de plata y bajo la luna', 'window': ' Sin miedo al silencio, el silencio nos habla Guitarras nos guían por caminos de plata y bajo la luna No buscamos luces que siguen por brillar y bajo la luna', 'prompt_window': 'Moonlit Pathways of Silver: Guitars Lead Us Through Whispering Silence Under a Celestial Canopy\n\nSilent pathways unfold like a silver river, guided by the gentle strumming of guitars. The lunar glow casts an ethereal light on the landscape, where shadows dance and whisper secrets to the wind. Amidst this mystical atmosphere, the silence is palpable, yet it holds a profound wisdom. Guitars weav their melodic threads through the stillness, leading us on a journey of introspection under the watchful eye of the celestial vault.'}, {'start': 35.0, 'end': 45.0, 'text': ' No buscamos luces que siguen por brillar y bajo la luna', 'window': ' Guitarras nos guían por caminos de plata y bajo la luna No buscamos luces que siguen por brillar y bajo la luna Caminamos sin pesar', 'prompt_window': '"Moonlit silver paths unfurl beneath a canvas of star-kissed night, as two wandering travelers follow the gentle guidance of guitars carried on worn leather straps. Silvery threads weave a tapestry of melody, as the pair ambles without concern, their footsteps light as whispers in the stillness. The landscape stretches out before them like a serene ocean, dotted with cypress trees that seem to whisper ancient secrets to the wind."'}, {'start': 46.0, 'end': 53.0, 'text': ' Caminamos sin pesar', 'window': ' No buscamos luces que siguen por brillar y bajo la luna Caminamos sin pesar No queremos glorias que solo sean fugaces y bajo la luna', 'prompt_window': "Under the silvery glow of a full moon, a lone wanderer treks across a desolate, moonlit landscape, with no need for fleeting lights or transitory glories. The traveler's footsteps are light and effortless, as if carried by the gentle night breeze. In the distance, a range of rugged mountains stretches out like dark, serrated teeth, their peaks still capped with wisps of cloud. A scattering of stars twinkles above, a celestial map guiding the wanderer's journey.\n\nIn this ethereal setting, the shadows themselves seem to have taken on a life of their own, twisting and curling like dark, liquid tendrils across the dusty terrain. The only sound is the soft crunch of gravel beneath the traveler's feet, and the distant hooting of an owl, its call echoing through the stillness like a mournful sigh.\n\nAs the wanderer walks, the landscape begins to take on a dreamlike quality, with rock formations assuming strange, surreal shapes, as if they too were being sculpted by the moon's silvery light. The air is cool and crisp, filled with the scent of dry earth and ozone, carrying the promise of adventure and discovery to the horizon."}, {'start': 53.0, 'end': 65.0, 'text': ' No queremos glorias que solo sean fugaces y bajo la luna', 'window': ' Caminamos sin pesar No queremos glorias que solo sean fugaces y bajo la luna', 'prompt_window': "A midnight stroll beneath a crescent moon casts an ethereal glow upon two friends wandering hand in hand through a lush meadow, their footsteps silent as they revel in each other's company. The sky above is ablaze with stars, like diamonds scattered across the velvet expanse. As they walk, wildflowers sway gently in the breeze, releasing a sweet fragrance that wafts around them. The landscape stretches out before them, a tapestry of greens and golds, punctuated by ancient trees that stand sentinel against the night sky."}]

    print(len(song_lyrics))

    f=calcular_f(song)
    print(f"frames: {f}")

    initial_state_a = "begin"
    initial_state_b = "silent"
    transitions_a = ["grow", "peak", "fade", "diminish", "end"]
    transitions_b = ["sparkle", "glisten", "twinkle", "quiet", "silent"]

    final=create_animation_structure(time, initial_state_a, initial_state_b, transitions_a, transitions_b)
    print(final)

    updated_structure = distribute_prompts(final, list_prompts)

    single_string_output = convert_to_single_string(updated_structure)
    
    return single_string_output , time , f

def song_to_video(song):
    single, tiempo, f =preproceso_prompt(song)
    print("------")
    print(single)
    print("------")
    print(tiempo)
    print("------")
    print(f)
    id=generate_random_15_digit_number()
    limit_frame = int(f)
    directory_path = f"C:\\Users\\jairc\\Pictures\\comfyui face\\ComfyUI\\output\\Audio-Reactive_{id}"
    limite= 3
    video=call_animediff(song,single, id, limit_frame,directory_path,limite)
    print(video)
    return video
    
def tiempo_intermedio(lista):
    list=[]
    n=0
    lista_redondeada = [round(elemento) for elemento in lista]
    while n <len(lista)-1:
        intermedio = round(int(lista[n+1])/2)
        list.append(intermedio)
        n += 1
    final=sorted(lista_redondeada + list)
    return final

def prompt_intermedio(lista_strings):
    nueva_lista = []
    for i, string in enumerate(lista_strings, start=1):
        nueva_lista.append(string)
        intermedio=stream_intermedio(string)
        nueva_lista.append(intermedio)
    return nueva_lista[:-1]

def preproceso_prompt_intermedio(song):
    song_lyrics = call_whisper(song)
    print(song_lyrics)
    list_prompts, full_prompt = call_window(song_lyrics)
    print("-------------------------------------------------")
    print(full_prompt)
    print("-------------------------------------------------")
    print(list_prompts)
    time = extract_time(full_prompt)
    print("-------------------------------------------------")
    print("primer refinamiento ")
    print("-------------------------------------------------")
    time = tiempo_intermedio(time)
    list_prompts = prompt_intermedio(list_prompts)
    """
    print("-------------------------------------------------")
    print("segundo refinamiento ")
    print("-------------------------------------------------")
    time = tiempo_intermedio(time)
    list_prompts = prompt_intermedio(list_prompts)
    
    """


    def remove_quotes(prompt):
        prompt = prompt.replace("\"", " ")
        prompt = prompt.replace("\n", " ").rstrip(", ")
        prompt = prompt.replace('"', '')
        prompt = prompt.replace("'", "")

        return prompt
    new_prompts=[]
    for e in list_prompts:
        new_prompts.append(remove_quotes(e))
        

    f = calcular_f(song)
    print(f"frames: {f}")

    initial_state_a = "begin"
    initial_state_b = "silent"
    transitions_a = ["grow", "peak", "fade", "diminish", "end"]
    transitions_b = ["sparkle", "glisten", "twinkle", "quiet", "silent"]

    final = create_animation_structure(time, initial_state_a, initial_state_b, transitions_a, transitions_b)
    print(final)

    updated_structure = distribute_prompts(final, new_prompts)

    single_string_output = convert_to_single_string(updated_structure)

    return single_string_output, time, f

def song_to_video_intermedio(song):
    single, tiempo, f =preproceso_prompt_intermedio(song)
    print("------")
    print(single)
    print("------")
    print(tiempo)
    print("------")
    print(f)
    id=generate_random_15_digit_number()
    limit_frame = int(f)
    directory_path = f"C:\\Users\\jairc\\Pictures\\comfyui face\\ComfyUI\\output\\Audio-Reactive_{id}"
    limite= 3
    video=call_animediff(song,single, id, limit_frame,directory_path,limite)
    print(video)
    return video
if __name__== "__main__":
    song= r"C:\Users\jairc\Downloads\Natanael-Cano_-Bzrp-Music-Sessions_-Vol.-59-_152kbit_Opus_.mp3"
    vid= song_to_video_intermedio(song)
    """
    song_lyrics=call_whisper(song)
    list_prompts,full_prompt=call_window(song_lyrics)
    print("full prompt")
    print(full_prompt)
    print("----------")
    print("list prompt")
    print(list_prompts)
    time=extract_time(full_prompt)
    print(time)
    """

    """
    prompt=['Astronaut lost in a swirling vortex of cosmic rock formations, surrounded by ethereal echoes of an abandoned astroplane, with stars and galaxies streaking across the dark sky.', 'Cosmic Odyssey: A swirling vortex of celestial hues envelops a lone astronaut lost amidst the depths of a glowing asteroid field, where echoes of an ancient astroplane whisper secrets to the cosmos.', 'Ethereal astroplane echoes swirl amidst a kaleidoscope of mindscapes, as jazz-infused drums orchestrate a rhythm that sets free the cosmic journey of self-discovery.', "A psychedelic odyssey unfolds as swirling colors of the mind's canvas merge with jazz-infused drums, setting a rhythm free from time's constraints: intricate patterns and shapes dance across the composition, evoking a sense of liberation and creative expression.", 'A swirling vortex of jazz-infused rhythms transports us to a kaleidoscope of worlds, where intricate drum patterns weave together in a mesmerizing dance of time signatures, as vibrant colors and shapes burst forth from the rhythmic collision.', 'A cosmic odyssey unfolds as intricate time signatures converge, transporting us across vast expanses of starry skies. Celestial guitars wail with mighty fervor, their ethereal melodies weaving a tapestry of sound that echoes through the vast expanse of space.', 'A celestial gathering: swirling galaxies converge as cosmic threads weave together, amidst a tapestry of shimmering stars and nebulae; guitars blaze with radiant energy, echoing through the void as figures dance beneath a kaleidoscope of aurora-lit skies.', 'A swirling galaxy of stars and nebulas serves as the backdrop for two figures dancing in mid-air, surrounded by a halo of ethereal light. Celestial guitars wail with mighty, otherworldly tones as they weave through the cosmic night, their melodic threads intertwining with the very fabric of space itself. Through the swirling vortex of colors and lights, the dancers ride the currents of sound, their forms blurring into one with the music as they disappear into the infinite expanse.', 'Dancing amidst swirling galaxies, we soar through the velvety darkness of space, guided by twinkling starlight as we navigate the cosmic vortex.', 'A cosmic odyssey unfolds as we soar through swirling vortex gates, with celestial bodies serving as our radiant compass, amidst an otherworldly realm where psychedelic energies course through the veins of a divine entity.', 'In a cosmic realm where celestial bodies converge with mystical energies, a psychedelic deity radiates an otherworldly glow amidst swirling starlight and nebulae, guiding us through the vast expanse of existence.']
    time=[0.0, 4.32, 10.88, 15.92, 24.0, 26.88, 35.76, 40.96, 46.56, 52.88, 58.800000000000004]
    time2=tiempo_intermedio(time)
    print(time2)
    prompts= prompt_intermedio(prompt)
    print("---")
    print(prompts)
    print(len(prompts))
    print(len(time2))
    """
    

    