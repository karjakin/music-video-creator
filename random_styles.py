import random

def generate_musical_style():
    # Definir las listas de palabras
    musical_styles = [
        "rock", "pop", "jazz", "blues", "classical", "hip hop", "reggae", "country", "folk", "electronic",
        "punk", "metal", "R&B", "disco", "funk", "soul", "salsa", "flamenco", "tango", "samba",
        "reggaeton", "cumbia", "bachata", "merengue", "bollywood", "k-pop", "j-pop", "afrobeat",
        "highlife", "gospel", "opera", "musical theater", "ambient", "new age", "world music",
        "celtic", "bluegrass", "acapella", "beatbox", "dub", "dubstep", "drum and bass", "hardstyle",
        "house", "techno", "trance", "trap", "lo-fi", "chillout", "bossa nova", "calypso", "zydeco"
    ]

    adjectives = [
        "energetic", "smooth", "soulful", "rhythmic", "melodic", "haunting", "uplifting", "emotional",
        "powerful", "gentle", "intense", "groovy", "catchy", "atmospheric", "experimental", "dreamy",
        "ethereal", "nostalgic", "romantic", "sensual", "mysterious", "hypnotic", "euphoric", "melancholic",
        "rebellious", "aggressive", "cheerful", "playful", "sophisticated", "exotic", "futuristic",
        "vintage", "minimalistic", "grandiose", "epic", "dynamic", "mellow", "gritty", "polished",
        "raw", "lush", "sparse", "dense", "airy", "warm", "cool", "bright", "dark"
    ]

    instruments = [
        "guitar", "piano", "saxophone", "drums", "violin", "bass", "trumpet", "flute", "harmonica",
        "accordion", "synthesizer", "banjo", "ukulele", "mandolin", "harp", "cello", "clarinet",
        "trombone", "tuba", "bagpipes", "didgeridoo", "sitar", "tabla", "bongos", "congas", "tambourine",
        "maracas", "xylophone", "vibraphone", "glockenspiel", "timpani", "orchestra", "choir", "turntables",
        "sampler", "theremin", "kalimba", "balalaika", "erhu", "koto", "shamisen", "duduk", "oud"
    ]

    # Generar una frase aleatoria
    phrase = random.choice([
        "The {adjective} {musical_style} with {instrument} solos!",
        "A fusion of {musical_style} and {musical_style}, featuring {instrument}.",
        "{musical_style} meets {musical_style} in this {adjective} composition.",
        "Experience the {adjective} sounds of {musical_style} with {instrument}.",
        "Immerse yourself in the {adjective} world of {musical_style} and {instrument}.",
        "Discover the {adjective} rhythms of {musical_style} infused with {instrument}.",
        "Let the {adjective} melodies of {musical_style} and {instrument} transport you.",
        "Feel the {adjective} energy of {musical_style} powered by {instrument}.",
        "Embrace the {adjective} fusion of {musical_style}, {musical_style}, and {instrument}.",
        "Dive into the {adjective} soundscapes of {musical_style} crafted with {instrument}.",
        "Savor the {adjective} harmonies of {musical_style} woven with {instrument}.",
        "Unleash the {adjective} power of {musical_style} driven by {instrument}.",
        "Indulge in the {adjective} textures of {musical_style} layered with {instrument}.",
        "Explore the {adjective} depths of {musical_style} enhanced by {instrument}."
    ])

    # Reemplazar los marcadores de posición con palabras aleatorias
    result = phrase.format(
        adjective=random.choice(adjectives),
        musical_style=random.choice(musical_styles),
        instrument=random.choice(instruments)
    )

    return result

# Ejemplo de uso
#print(generate_musical_style())