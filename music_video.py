
from urllib import request, error
import json
import random
import os
import time


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

json_file_path = r'E:\code\music\animediff_api2.json'

with open(json_file_path, 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

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

def generate_random_15_digit_number():
    return random.randint(100000000000000, 999999999999999)

def animediff(path,prompt, id, limit_frame,directory_path):
    print(prompt)
    print(limit_frame)
    neg_prompts="(deformed, distorted, disfigured:1.25), poorly drawn, bad anatomy, wrong anatomy, extra limb, missing limb, floating limbs, (mutated hands and fingers:1.3), disconnected limbs, mutation, mutated, blurry, amputation::0.6, necklace, nude, nsfw, canvas frame, out-of-frame, ugly, cross-eyed, woman,man, person"

   
    # Create directory
    os.makedirs(directory_path, exist_ok=True)
    print(f"Directory created at {directory_path}")
    data["4"]["inputs"]["ckpt_name"] = "picxReal_10.safetensors"
    data["302"]["inputs"]["limit_frames"] = limit_frame
    data["445"]["inputs"]["limit_frames"] = limit_frame
    data["316"]["inputs"]["audio"] = path
    data["438"]["inputs"]["audio_file"] = path
    data["472"]["inputs"]["text_a"] = " "
    data["473"]["inputs"]["text_a"] = " "
    data["268"]["inputs"]["text"] = prompt
    data["436"]["inputs"]["text"] = neg_prompts
    data["437"]["inputs"]["filename_prefix"] = f"Audio-Reactive_{id}/song2vid"
    data["148"]["inputs"]["value"] = 512
    data["149"]["inputs"]["value"] = 768

    
    queue_prompt(data)  


def call_animediff(list_path,prompt, id, neg_prompts,directory_path,limite):
    json_output_path = "output3.json"
    animediff(list_path,prompt, id, neg_prompts,directory_path)    
    output=monitor_directory(directory_path,limite,json_output_path)
    print(output)
    return output

if __name__ == "__main__":

    prompt="""
    "0": "(begin:`pw_a`),(silent:`pw_b`), A serene tropical beach at sunset: warm golden light casts long shadows on powdery white sand, where a pair of toes wiggle with joy. The air is alive with the rhythm of waves gently lapping at the shore, as seagulls soar overhead, their cries harmonizing with the melody. A slice of paradise, where the soothing sounds and scents of the ocean converge to transport the viewer to a state of bliss. Camera angle: low-angle shot from above, capturing the toes in mid-wiggle; focal length: 50mm; composition: leading lines of sand and waves guide the eye to the toes.",
    "47": "(peak:`pw_a`),(sparkle:`pw_b`), A sun-kissed beach scene: between the toes of a majestic sandcastle, I'm in paradise. Feel the rhythm of waves gently lapping at the shore, it's a slice of serenity. Drop of vibrant seaglass and contagious energy swirl around, as if infused by the air itself.",
    "94": "(peak:`pw_a`),(glisten:`pw_b`), A kaleidoscope of vibrant fagabondia swirls around a mesmerizing drop of energy, radiating contagious rhythm and inviting dance. Amidst a backdrop of swirling purple and orange hues, iridescent shapes burst forth in shimmering silver and gold, as if the music itself has taken on a life of its own. The air is electric with pulsing beats, as if the very essence of the song has been distilled into this whimsical, dreamlike scene. Capture the frenetic energy from a low-angle shot, emphasizing the dynamic shapes and colors that seem to defy gravity, while the camera's shallow depth of field blurs the background, keeping focus on the mesmerizing drop of vives at the center.",
    "127": "(peak:`pw_a`),(twinkle:`pw_b`), Vibrant fagabondia unfurls like a tapestry of iridescent petals, swaying to the rhythm of contagious energy as warm sunlight dances across its delicate curves. Amidst a backdrop of wispy clouds and cerulean sky, CRIS's gentle breeze whispers secrets to the flowers, causing them to sway in perfect harmony. The air is alive with the sweet scent of blooming wildflowers, drawing in passersby like moths to a flame. As the camera pans across this whimsical scene, focus on the intricate details of the fagabondia's petals and the way they seem to shimmer in the sunlight.",
    "196": "(peak:`pw_a`),(quiet:`pw_b`), Vibrant fagabondia bloom amidst whimsical, swirling patterns, as Breezy Schmalt's delicate petals sway in the warm sunlight. Every moment here, CRIS's tender shoots seem to pulse with life, their gentle dance illuminated by a kaleidoscope of colors: soft pinks, sunshine yellows, and sky blues.",
    "241": "(peak:`pw_a`),(silent:`pw_b`), A vibrant CRIS sculpture, Breezy Schmalt, sways gently in the warm sunlight, its delicate petals dancing like ballerinas on a sun-kissed meadow. The surrounding air is alive with the sweet scent of blooming flowers and the soft hum of insects, as the gentle breeze whispers secrets to the sculpture's intricate curves.",
    "296": "(peak:`pw_a`),(sparkle:`pw_b`), A vibrant, pulsating cityscape at dusk, with neon lights reflecting off wet pavement. A sprawling mural of Vagabondía's iconic music notes and instruments comes alive on the side of a building, as if beckoning passersby to join the celebration. The air is electric with anticipation, as confetti and balloons swirl around a giant, glowing speaker system. Every moment feels alive, as the rhythm pulses through the streets, drawing in people from all walks of life. Capture this energetic scene from a low angle, looking up at the mural, with a wide-angle lens to emphasize the sense of community and freedom.",
    "342": "(peak:`pw_a`),(glisten:`pw_b`), Vibrant Vagabondia: A Night of Unbridled Joy - A swirling vortex of colors and lights envelops the scene as a lone dancer, dressed in a flowing red dress with intricate silver embroidery, twirls with abandon. Her hair flows like a fiery mane, and her eyes sparkle like diamonds under the strobe lights. The music pulses through the air, a rhythmic heartbeat that draws the viewer in. In the background, neon-lit cityscapes and abstract shapes blur together, a kaleidoscope of urban energy. Camera angle: low-angle shot from directly below, capturing the dancer's dynamic movement and emphasizing her freedom. Focal length: wide-angle lens to encompass the vibrant atmosphere. Composition: radial symmetry around the dancer, with lights and colors radiating outward like ripples on a pond.",
    "399": "(peak:`pw_a`),(twinkle:`pw_b`), Vibrant Vagabondia: A Whimsical Dance of Colors, where swirling purple mist envelops a majestic, glowing guitar, its strings vibrating with an ethereal melody. Amidst the fog, a kaleidoscope of butterflies in shades of turquoise, amber, and crimson dance, their iridescent wings shimmering as they twirl around the instrument. The air is filled with glittering, shimmering sparks that seem to take on a life of their own, swirling around the guitar like a mesmerizing vortex. Camera angle: A low-angle shot from above, capturing the dynamic movement of the butterflies and the hypnotic glow of the guitar. Focal length: Wide-angle lens to emphasize the expansive, dreamlike quality of the scene. Composition: The guitar serves as a central anchor, with the swirling mist and dancing butterflies radiating outward in a vibrant, symphonic dance.",    
    "452": "(peak:`pw_a`),(quiet:`pw_b`), A vibrant, whimsical illustration of a free-spirited En Vibrante Vagabondía, surrounded by swirling clouds of iridescent purple and blue, as she dances with reckless abandon under a starry night sky. Her wild, curly hair flows like a river of gold, and her eyes shine bright with an inner light. In the background, a cityscape stretches out in a kaleidoscope of colors, with neon lights and billboards blending into a mesmerizing haze. The camera zooms in on En Vibrante's ecstatic expression, capturing the pure joy and abandon as she loses herself to the music.",
    "535": "(peak:`pw_a`),(silent:`pw_b`), In Vibrant Vagabondia's swirling vortex, a kaleidoscope of colors converges: turquoise wisps curl around crimson petals, while emerald leaves dance amidst amber hues. The air vibrates with ecstatic energy as the music swirls, a mesmerizing whirlpool drawing in stray notes and rhythms like moths to a flame. Amidst this whirlwind, a lone guitar weaves its melodic magic, strings singing with an otherworldly voice.Camera angle: Aerial view from above, capturing the swirling colors and shapes as they coalesce into a vibrant tapestry. Focal length: Wide-angle lens to encompass the entire scene, emphasizing the dynamic movement and energy. Composition: The guitar becomes the central axis, with colors and patterns radiating outward like ripples on a pond.",
    "588": "(peak:`pw_a`),(sparkle:`pw_b`), A vibrant, swirling vortex of color erupts on a moonlit dance floor, as pulsing rhythms and melodies swirl around a mesmerizing, ethereal Vagabondía. Delicate, iridescent wings unfurl from her back, shimmering with an otherworldly glow. With eyes closed, she surrenders to the ecstasy of the music, her slender form undulating in time with the beat. Amidst the whirling chaos, a kaleidoscope of lights and patterns dance across the floor, refracting through prismatic shards of glass and crystal. Capture the scene from a low angle, looking up at Vagabondía as she twirls, her wings beating in slow motion, with the camera positioned to emphasize the swirling colors and textures around her.",
    "714": "(peak:`pw_a`),(glisten:`pw_b`), Vibrant Vagabondia: A whimsical, fiery gypsy wagon, adorned with tassels and lanterns, is parked amidst a lush, emerald-green forest. Riches overflow from its open doors, spilling onto the forest floor in glittering piles of gold coins, precious jewels, and ancient artifacts. The air is alive with the scent of exotic spices and the soft strumming of a lone guitar. As the sun sets behind the trees, the wagon's vibrant colors seem to pulse with an inner light, beckoning passersby to join the revelry.",
    "742": "(peak:`pw_a`),(twinkle:`pw_b`), A whimsical hot air balloon soars above a kaleidoscope of vibrant vagabondia, its basket overflowing with golden coins and precious jewels. The balloon's canopy is adorned with intricate, swirling patterns that shimmer like stained glass windows in the warm sunlight. As it drifts lazily across the sky, the wind whispers secrets to the balloon's delicate gondola, which responds by releasing a trail of glittering sparks that fade into the distance. In the foreground, a tumbleweed rolls down a dusty path, its dry branches crackling with every step. The air is filled with the sweet scent of blooming wildflowers and the distant chime of a lone wind chime. Capture this scene from a low-angle shot, looking up at the balloon as it floats above the vibrant landscape, with the tumbleweed and wildflowers framing the composition.",
    "1051": "(peak:`pw_a`),(quiet:`pw_b`), A whimsical illustration of Vibrant Vagabondia unfolds, where a majestic hot air balloon, adorned with shimmering golden accents and vibrant floral patterns, soars above a lush, emerald-green landscape. The balloon's basket is overflowing with colorful lanterns, fluttering ribbons, and exotic flowers, as if the very essence of adventure has been distilled within. In the distance, a winding road disappears into the rolling hills, lined with ancient trees heavy with golden leaves. As the sun sets behind the balloon, its fiery hues dance across the sky, casting a warm glow on the entire scene. Camera angle: Aerial view from above, capturing the balloon's majestic form against the vibrant landscape. Focal length: Wide-angle to emphasize the sense of freedom and adventure. Composition: The balloon is centered, with the landscape and road leading the viewer's eye towards the horizon.",
    "1147": "(peak:`pw_a`),(silent:`pw_b`), In vibrant vagabondia, where sunset hues of saffron and amber dance across the sky, a whimsical procession of hot air balloons, adorned with fluttering ribbons and lanterns, sway gently to an unseen rhythm. The balloons' shapes evoke fantastical creatures, their colors blending in a mesmerizing swirl of turquoise, crimson, and gold. As the music wafts through the air, the balloons seem to come alive, their silken strands undulating like a chorus of ethereal dancers. In the distance, a range of mystical mountains rises, their peaks shrouded in mist, as if beckoning the viewer to join the enchanting journey. Capture this moment from a low-angle shot, with the balloons suspended above the horizon, and the mountains looming in the background, conveying a sense of wonder and limitless possibility.",
    "1207": "(peak:`pw_a`),(sparkle:`pw_b`), A whimsical twilight dance party unfolds amidst a vibrant vagabondia, where fluttering lanterns and twinkling fireflies illuminate the air. The scent of blooming flowers wafts through the scene as a kaleidoscope of colorful fabric sways in rhythm with the music's pulsing beat. Delicate petals unfurl like tiny ballerinas, their gentle dance echoing the carefree joy of the melody. As the camera swoops in from above, the vibrant hues and textures blend together in a mesmerizingemerald and amethyst. Delicate petals of flowers dance in mid-air, as if beckoning passersby to join the revelry. Amidst this whimsical backdrop, a majestic tree stands tall, its branches adorned with glittering lanterns that seem to pulse with an otherworldly energy. The air is alive with the sweet scent of blooming wildflowers and the soft hum of enchanted insects. Come dance with me, as the phrase whispers, amidst this kaleidoscope of wonder."
    """

    id=generate_random_15_digit_number()
    limit_frame= 787
    directory_path = f"C:\\Users\\jairc\\Pictures\\comfyui face\\ComfyUI\\output\\Audio-Reactive_{id}"
    limite= 3
    path=r"C:\\Users\\jairc\\Downloads\\Caminos20Plata.mp3"

    video=call_animediff(path,prompt, id, limit_frame,directory_path,limite)