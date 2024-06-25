import pandas as pd
import csv
from Ollamaprompt import stream_ollama_response
def extraer_columnas_completas(csv_filename):
    # Leer el archivo CSV
    df = pd.read_csv(csv_filename, sep='\t')  # Utilizando el separador correcto, en este caso parece ser un tabulador '\t'
    
    # Si necesitas la información en forma de listas
    columna_1 = df.iloc[0, 0]  # Convertir la primera columna en lista
    columna_2 = df.iloc[1, 0] # Convertir la segunda columna en lista
    
    return columna_1, columna_2

def agregar_nueva_fila_al_inicio(archivo, cadena):
    # Leer el archivo CSV con pandas
    df = pd.read_csv(archivo)
    
    # Crear un nuevo DataFrame con la cadena como primera fila
    nueva_fila = pd.DataFrame([[cadena] + [None] * (df.shape[1] - 1)], columns=df.columns)
    
    # Concatenar el nuevo DataFrame con el existente
    df_nuevo = pd.concat([nueva_fila, df]).reset_index(drop=True)
    
    # Guardar los cambios en el archivo CSV
    df_nuevo.to_csv(archivo, index=False)
    print("--------")
    print("Se ha agregado una nueva fila al inicio del archivo.")

# Ejemplo de uso
archivo_csv = 'musica.csv'

columna_1, columna_2=extraer_columnas_completas(archivo_csv)
print(columna_1)
print("------------")
print(columna_2)
print("------------")
columna_join=columna_1.join(columna_2)
output=stream_ollama_response(columna_join)
print("--------")
print(output)
prompt = output
agregar_nueva_fila_al_inicio(archivo_csv, prompt)
