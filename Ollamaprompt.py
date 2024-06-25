from langchain_community.llms import Ollama
from langchain_community.chat_models import ChatOllama
import sys
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from random_styles import generate_musical_style
from langchain_core.prompts import ChatPromptTemplate
import os
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
os.environ['LANGCHAIN_API_KEY'] = "ls__6d685e614085499b93d8358895005721"
def add_text(start_text, end_text, middle_text):

    return f"{start_text} {middle_text} {end_text}"

template_intermedio="""
<|start_header_id|>system<|end_header_id|>
You are an AI assistant highly skilled at generating vivid descriptions,Your goal is to create intermedian prompts for creative illustrations

<|eot_id|>

<|start_header_id|>user<|end_header_id|>
Please generate a rich, detailed description, that illustrates the lyrics of a song, use this phrase as a reference
Your goal is to create the next prompt based on the last prompt.
passed prompt: {input}
you have to vary the past prompt in an interesting and novel way
improve simple prompts for image generation, making them more detailed, rich, and visually interesting.
condense all that information into a single short prompt
only returns the improved prompt in english dont add any extra coment

<|eot_id|><|start_header_id|>assistant<|end_header_id|>

"""
template_window="""
<|start_header_id|>system<|end_header_id|>
You are an AI assistant highly skilled at generating vivid descriptions,Your goal is to create prompts for creative illustrations

<|eot_id|>

<|start_header_id|>user<|end_header_id|>
Please generate a rich, detailed description, that illustrates the lyrics of a song, use this phrase as a reference

phrase:  ////{input}////

Identify the central theme of the original phrase. 
Add specific details about the main subjects, such as color, shape, activity, and expression.
Introduce contextual elements that complement the scene without diverting attention from the main subject.
Suggest different camera angles, focal lengths or compositions. Maintain consistency of style and tone of the original prompt. 
Don't alter the central theme, just enrich what is already present. Respect ethical and legal guidelines. avoid placing people.

condense all that information into a single short prompt
only returns the improved prompt in english dont add any extra coment

<|eot_id|><|start_header_id|>assistant<|end_header_id|>

"""
template_window2="""
<|start_header_id|>system<|end_header_id|>
You are an AI assistant highly skilled at generating vivid descriptions,Your goal is to create prompts for creative illustrations,
only returns the improved prompt in english dont add any extra coment, condense all that information into a single short prompt
<|eot_id|>
<|start_header_id|>user<|end_header_id|>
Please generate a rich, aesthetic , detailed description, based on the lyrics of the song, use this phrase as a reference
{input}
improve simple prompts for image generation, making them more detailed, rich, and visually interesting.
condense all that information into a single short prompt
only returns the improved prompt in english dont add any extra coment
<|eot_id|><|start_header_id|>assistant<|end_header_id|>

"""
template_window_dolphin="""
<|im_start|>system
You are an AI assistant highly skilled at generating vivid descriptions,Your goal is to create prompts for creative illustrations,
only returns the improved prompt in english dont add any extra coment, condense all that information into a single short prompt
<|im_end|>
<|im_start|>user
Please generate a rich, aesthetic , detailed description, based on the lyrics of the song, use this phrase as a reference
{input}
improve simple prompts for image generation, making them more detailed, rich, and visually interesting.
condense all that information into a single short prompt
only returns the improved prompt in english dont add any extra coment
<|im_end|>
<|im_start|>assistant

"""
template = """

Identify the Central Theme: Determine the main subject of the original prompt.

Add Specific Details: Enrich the prompt with specific details about the main subjects, such as color, shape, activity, expression.

Introduce Context Elements: Add background or context elements that complement the scene without diverting attention from the main subject.

Vary Perspective and Composition: Suggest different camera angles, focal lengths or compositions to give a new dimension to the prompt.

Maintain Style Consistency: Make sure the added details align with the style and tone of the original prompt (e.g., realistic, whimsical, abstract).

Avoid Changing the Original Theme: Do not alter the central theme of the prompt, only enrich what is already present.

Include Diversification and Avoid Biases: Make sure that representations of people are diverse and avoid stereotypes or biases.

Respect Ethical and Legal Guidelines: Avoid adding elements that may be offensive, problematic 

improve simple prompts for image generation, making them more detailed, rich, and visually interesting.
the output is always in English even though the input is in Spanish
condense all that information into a single medium-sized prompt
only returns the improved prompt in english
User input: {input}
only returns the improved prompt in english dont add any extra coment

"""

template_command="""
<|START_OF_TURN_TOKEN|><|SYSTEM_TOKEN|>
Objective: Your task is to design a unique music prompt that builds upon the themes and styles of the previously created songs listed below:

{input}

do not repeat the original phrases, be creative, expand and invent
use key works, Be direct, output just a string whit the final prompt, dont add any extra coment
<|END_OF_TURN_TOKEN|>
<|START_OF_TURN_TOKEN|><|USER_TOKEN|>
instructions:
Reflect on Past Creations: Review the provided songs to understand their themes, genres, and musical characteristics.
Innovate: Create variations by blending elements from these songs with new genres or unique musical combinations.
Expand Horizons: Explore unconventional or underrepresented music genres to infuse freshness into your creation.
Experiment: Feel free to mix different instruments, rhythms, and vocal styles to craft a diverse and engaging musical experience.
Goal: Produce a music prompt that is both reflective of past works and innovative, paving the way for fresh and captivating music creations.
use key works, Be direct, middle distant, output just a string whit the final prompt, dont add any extra coment

<|END_OF_TURN_TOKEN|><|START_OF_TURN_TOKEN|><|CHATBOT_TOKEN|>
"""

template_gen_llama3="""
<|start_header_id|>system<|end_header_id|>
You are an AI assistant highly skilled at generating vivid descriptions of various musical styles. You have an encyclopedic knowledge of music genres, subgenres. Your descriptions capture the key characteristics, instrumentation, rhythms, melodies, lyrical themes, and emotions associated with each style. You can generate an evocative overview of any musical style requested.
do not use explicit artist names or songs names
use style key works, Be direct, don't add any extra coment ,create a short prompt, only output the enhance prompt
<|eot_id|>

<|start_header_id|>user<|end_header_id|>
Please generate a rich, detailed description of the defining characteristics of a new musical style, as if you were explaining it to someone who had never heard it before: 
use key works style:
{input}
The description should cover:

Instrumentation, music styles
Rhythmic feel and tempo
Melodic and harmonic traits
Lyrical themes and vocal styles
don't add categories, just write a continuous prompt
use style key works, Be direct, don't add any extra coment ,create a short prompt, only output the new prompt
create a direct and a very short prompt
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
"""
template_gen_llama3_simple2="""
<|start_header_id|>system<|end_header_id|>
You are an AI assistant skilled at generating vivid descriptions of songs ,your output is musical style and lyrical themes. Your descriptions capture the key characteristics of the song's style and the main themes of the lyrics. You can generate style keywords and lyrical theme.
allways output short prompts
<|eot_id|>

<|start_header_id|>user<|end_header_id|>
Please generate a rich, detailed description of a song with the following characteristics:

Musical style keywords: {input} random, invent the keywords, create a new song, be creative
Lyrical theme: The lyrics should be thematically related to the song's style and convey a message or story that fits the musical mood.

Your description should include:
- The overall musical atmosphere and emotions evoked by the song
- Key instrumentation and musical elements that define the song's style
- A brief overview of the lyrical content and how it relates to the song's style
do not use categories, just a simple continuous prompt
Use style keywords, be direct, and create a concise and dense prompt. Only output the new prompt without any extra comments.
output a very short prompt
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
"""
template_gen_llama3_simple="""
<|start_header_id|>system<|end_header_id|>
You are an AI assistant skilled at generating vivid descriptions of songs ,your output is musical style and lyrical themes. Your descriptions capture the key characteristics of the song's style and the main themes of the lyrics. You can generate style keywords and lyrical theme.
allways output short prompts
<|eot_id|>

<|start_header_id|>user<|end_header_id|>
Please generate a rich, detailed description of a song with the following characteristics:

Musical style keywords: {input} random, invent the keywords, create a new song, be creative
Lyrical theme: The lyrics should be thematically related to the song's style and convey a message or story that fits the musical mood.

Your description should include:
- The overall musical atmosphere and emotions evoked by the song
- Key instrumentation and musical elements that define the song's style
- A brief overview of the lyrical content and how it relates to the song's style
do not use categories, just a simple continuous prompt
Use style keywords, be direct, and create a concise and dense prompt. Only output the new prompt without any extra comments.
output a very short prompt
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
"""

template_gen_llama3_simple_dolphin="""
<|im_start|>system
You are an AI assistant skilled at generating vivid descriptions of songs ,your output is musical style and lyrical themes. Your descriptions capture the key characteristics of the song's style and the main themes of the lyrics. You can generate style keywords and lyrical theme.
allways output short prompts
<|im_end|>

<|im_start|>user
Please generate a rich, detailed description of a song with the following characteristics:

Musical style keywords: invent the keywords, create a new song, be creative {input} 
Create a new combination of style, explore musical genres, with coherent combinations among themselves.
Lyrical theme: The lyrics should be thematically related to the song's style and convey a message or story that fits the musical mood.

Your description should include:
- The overall musical atmosphere and emotions evoked by the song and key instrumentation and musical elements that define the song's style
- A brief overview of the lyrical content and how it relates to the song's style
do not use categories, just a simple continuous prompt
Use style keywords, be direct, and create a concise and dense prompt, dont use spaces. Only output the new prompt without any extra comments.
output a very short prompt
<|im_end|>
<|im_start|>assistant
"""
prompt_intermedio = ChatPromptTemplate.from_template(template_intermedio)
prompt_window = ChatPromptTemplate.from_template(template_window)
prompt = ChatPromptTemplate.from_template(template_gen_llama3_simple2)
#llm = Ollama(model="llama3:70b-instruct-q4_0",temperature=1)
#llm = Ollama(model="llama3:70b-instruct-q3_K_M")
#llm = Ollama(model="llama3:70b-instruct-q2_K",temperature=1)
llm = Ollama(model="llama3:8b-instruct-fp16",temperature=0.4)
llm2 = Ollama(model="llama3:8b-instruct-fp16",temperature=0.2)
#llm = Ollama(model="dolphin-llama3:8b-v2.9-fp16",temperature=0.4)
#llm = Ollama(model="wizardlm2:7b-fp16")
#llm = Ollama(model="command-r:latest")
output_parser = StrOutputParser()
chain_gen = ({"input": RunnablePassthrough()}
    | prompt 
    | llm2
    | output_parser
         ) 
chain_window = ({"input": RunnablePassthrough()}
    | prompt_window
    | llm
    | output_parser
         ) 
chain_intermedio= ({"input": RunnablePassthrough()}
    | prompt_intermedio
    | llm
    | output_parser
         ) 
separador="""

-------------------

"""
def stream_gen(query):
    chunks = []
    complete_response = ""
    for chunk in chain_gen.stream(query):
        print(chunk, end='', flush=True)
        complete_response += chunk
        chunks.append(chunk)
        if '<|eot_id|>' in chunk:
            print(separador)   
            break  
    output = complete_response.strip().replace("<|eot_id|>", "")
    return output 

def stream_window(query):
    chunks = []
    complete_response = ""
    for chunk in chain_window.stream(query):
        print(chunk, end='',flush=True)
        complete_response += chunk
        chunks.append(chunk)
        if '<|eot_id|>' in chunk:
            print(separador)  
            break  
    output = complete_response.strip().replace("<|eot_id|>","")
    return output 

def stream_intermedio(query):
    chunks = []
    complete_response = ""
    for chunk in chain_intermedio.stream(query):
        print(chunk, end='',flush=True)
        complete_response += chunk
        chunks.append(chunk)
        if '<|eot_id|>' in chunk:
            print(separador) 
            break  
    output = complete_response.strip().replace("<|eot_id|>","")
    return output 


llama3_templete=add_text("<|start_header_id|>user<|end_header_id|>","<|eot_id|><|start_header_id|>assistant<|end_header_id|>",template )
wizardlm2_templete=add_text("USER: ","ASSISTANT: ",template )
command_r_templete=add_text("<|START_OF_TURN_TOKEN|><|USER_TOKEN|>","<|END_OF_TURN_TOKEN|><|START_OF_TURN_TOKEN|><|CHATBOT_TOKEN|>",template )

if __name__== "__main__":

    """
    print("--------")
    output=stream_ollama_response("electronic, synthesizer, synth-pop, house, downtempo, ambient")
    print(output)
    print("--------")

    example="Celtic Disco,Thrash metal, Synthwave Gospel, Post-rock, Afrobeat Blues, Rockabilly House, Klezmer, Ambient Dub, Pirate Pop Punk, Electroswing Fusion"
    output=stream_gen(example)
    print(output)
    
    example="Caminamos sin risa con el alma desnuda Abrazando recuerdos en el viento se acunan Sin miedo al silencio, el silencio nos habla"
    output=stream_window(example)
    print(output)

    example=" "
    output=stream_gen(example)
    print(output)
    
    

    example="Caminamos sin risa con el alma desnuda Abrazando recuerdos en el viento se acunan Sin miedo al silencio, el silencio nos habla"
    
    print("-------")
    output=stream_window(example)
    print("-------")
    """

    example=generate_musical_style()
    print(example)
    output=stream_gen(example)
    #print(output)
    """
    example="Caminamos sin risa con el alma desnuda Abrazando recuerdos en el viento se acunan Sin miedo al silencio, el silencio nos habla"
    
    print("-------")
    output=stream_window(example)
    print("-------")
    """

    
    

