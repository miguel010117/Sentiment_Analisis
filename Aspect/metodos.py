import csv
import torch
from nltk import sent_tokenize
from torch import nn
import re
from extraccion_aspect import *

class ModelSentiment(nn.Module):

    def __init__(self, n_classes):
        super(ModelSentiment, self).__init__()

    def forward(self, input_ids, attention_mask):
        cls_output = self.model(input_ids, attention_mask)
        drop_output = self.drop(cls_output.pooler_output)
        output = self.linear(drop_output)
        return output


# Lee el archivo CSV y extrae las opiniones de la columna especificada.
def procesar_archivo(ruta_archivo):

    opiniones = []
    with open(ruta_archivo, "r", encoding="utf-8") as archivo_csv:
        lector_csv = csv.reader(archivo_csv)
        # Asumir que las opiniones están en la primera columna (índice 0)
        for fila in lector_csv:
            opiniones.append(fila[0])
    return opiniones


# Extraer solo las opiniones donde existan palabras claves (Aspectos)
def extraer_opiniones_relevantes(opiniones,palabras):
    opiniones_relevantes = []
    for opinion in opiniones:
        for palabra in palabras:
            if re.search(r"\b" + palabra + r"\b", opinion):
                opiniones_relevantes.append(opinion)
                break
    return opiniones_relevantes

# LLenar el achivo csv de salida con todos sus datos
def llenar_archivo_salida(model,tokenizer,opiniones, palabras_clave):
    # Nombre del archivo CSV
    nombre_archivo = "datos_salida.csv"

    # Cargar el archivo CSV (crear si no existe)
    with open(nombre_archivo, "a", newline="", encoding="utf-8") as archivo_csv:
        escritor_csv = csv.writer(archivo_csv,delimiter=';')

        # LLenar el archivo
        for opinion in opiniones:
            
            oraciones = extraer_oraciones_relevantes(opinion,palabras_clave)
            
            for oracion, palabras in oraciones.items():
                for i in range(len(palabras)):
                    segmento = extraer_segmento(oracion,palabras[i])
                    polarity = sentiment_analisis(model,tokenizer,segmento)
                    escritor_csv.writerow([opinion, oracion, palabras[i],segmento,polarity]) 
            

# Extraer solo las oraciones donde existan palabras claves (Aspectos)
def extraer_oraciones_relevantes(opinion, palabras_clave):
    print("1", opinion)
    # Dividir la opinión en oraciones
    oraciones = sent_tokenize(opinion)
    print("2",oraciones)
    # Analizar cada oración
    resultados = {}
    for oracion in oraciones:
        palabras_encontradas = []
        for palabra_clave in palabras_clave:
            if re.search(r"\b" + palabra_clave + r"\b", oracion):
                palabras_encontradas.append(palabra_clave)
            
        if palabras_encontradas:  # Solo si se encontraron palabras clave
            resultados[oracion] = palabras_encontradas 


    return resultados


#Funcion para crear el encoding
def encoding(model,tokenizer,review):
    encoding_review = tokenizer.encode_plus(
        review,
        add_special_tokens = True,
        max_length = 250,
        padding = "max_length",
        return_token_type_ids = False,
        truncation = True,
        return_attention_mask = True,
        return_tensors = 'pt'
    )
    input_ids = encoding_review['input_ids']
    attention_mask = encoding_review['attention_mask']
    output = model(input_ids,attention_mask)
    _, prediction = torch.max(output,dim=1)

    return prediction

# Clasificador de opinion
def sentiment_analisis(model,tokenizer,review_text):
    prediction = encoding(model,tokenizer,review_text)
    if prediction:
        return "Positivo"
    else:
        return "Negativo"