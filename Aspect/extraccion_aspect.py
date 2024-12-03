import spacy
import re
# Cargar el modelo en español de spaCy
nlp = spacy.load("es_core_news_sm")  

# Dada la oracion y el aspecto extrae el segmento donde se encuentra el aspecto
def extraer_segmento(oracion,aspecto):
    dependencias = extraer_dependencias(oracion, aspecto)
    lista = palabras_sin_repetir(dependencias)
    segmento = combination(oracion,lista)

    return convertir_lista_oracion(segmento)

def extraer_dependencias(texto_opinion, palabra_clave):


    doc_analizado = nlp(texto_opinion)
    frases_extraidas = []

    for palabra_actual in doc_analizado:
        if palabra_actual.text == palabra_clave:
            palabras_asociadas = []
            
            # Extraer palabras a la izquierda y derecha de la palabra clave
            palabras_asociadas.extend(extraer_palabras_izquierda(palabra_actual))
            palabras_asociadas.append(palabra_actual.text)
            palabras_asociadas.extend(extraer_palabras_derecha(palabra_actual))

            palabra_principal = palabra_actual.head

            # Extraer sujetos y objetos directos relacionados con la palabra principal
            palabras_asociadas.extend(extraer_palabras_izquierda(palabra_principal))
            palabras_asociadas.append(palabra_principal.text)
            palabras_asociadas.extend(extraer_palabras_derecha(palabra_principal))

            # Agregar n-gramas, contexto y la frase extraída
            frases_extraidas.append(n_gramas(texto_opinion, palabra_clave, 3))
            frases_extraidas.append(extraccion_contexto(texto_opinion, palabra_clave))
            frases_extraidas.append(palabras_asociadas)

    return frases_extraidas

# Funciones auxiliares para extraer dependencias

def extraer_palabras_izquierda(palabra_actual):
    palabras = []
    for palabra_relacionada in palabra_actual.lefts:
        palabras.append(palabra_relacionada.text)
        if palabra_relacionada.dep_ in ['NOUN']:
            for x in palabra_relacionada.lefts:
                if x.dep_ in ['ADJ']:
                    palabras.append(x.text)

            for x in palabra_relacionada.rights:
                if x.dep_ in ['ADJ']:
                    palabras.append(x.text)
    return palabras

def extraer_palabras_derecha(palabra_actual):
    palabras = []
    for palabra_relacionada in palabra_actual.rights:
        palabras.append(palabra_relacionada.text)
        if palabra_relacionada.dep_ in ['NOUN']:
            for x in palabra_relacionada.lefts:
                if x.dep_ in ['ADJ']:
                    palabras.append(x.text)

            for x in palabra_relacionada.rights:
                if x.dep_ in ['ADJ']:
                    palabras.append(x.text)
    return palabras













def extraccion_contexto(oracion, palabra_relevante):
    doc = nlp(oracion)
    token_palabra_relevante = None
    for token in doc:
        if token.text.lower() == palabra_relevante:
            token_palabra_relevante = token
            break

    if not token_palabra_relevante:
        return "Palabra relevante no encontrada en la oración"

    modificadores = []
    for token in doc:
        if token.head == token_palabra_relevante and token.dep_ in ["amod", "advmod", "nsubj", "nummod", "det"]:
            modificadores.append(token.text)
    
    return modificadores


def n_gramas(oracion, palabra, numero):
    print(oracion)
    print(palabra)
    palabras = limpiar_oracion(oracion).split()  # Dividir la oración en palabras
    index_palabra = []


    for index, word in enumerate(palabras):

        if word.lower() == palabra.lower() :
            index_palabra = index
            break

    palabras_anteriores = palabras[max(0, index_palabra - numero):index_palabra]
    palabras_posteriores = palabras[index_palabra + 1:index_palabra + 1 + numero]

    return palabras_anteriores + [palabra] + palabras_posteriores


def limpiar_oracion(oracion):

    # Usar una expresión regular para encontrar y reemplazar todos los caracteres que no sean letras
    oracion_limpia = re.sub(r'[^a-zA-Z\sáéíóúüÁÉÍÓÚÜñÑ]', ' ', oracion) 

    # Devolver la oración limpia
    print(oracion_limpia)
    return oracion_limpia


def palabras_sin_repetir(lista_de_listas):
    palabras = set()  # Utilizamos un conjunto para evitar palabras duplicadas
    
    for sublista in lista_de_listas:
        for palabra in sublista:
            palabras.add(palabra)  # Convertimos las palabras a minúsculas para evitar duplicados

    return list(palabras)  # Convertimos el conjunto de palabras de nuevo a una lista y la devolvemos



def combination(oracion, list):
    result = []
    for token in oracion.split():
        if (token in list) or (token[0:-1] in list):
            if not token in result:
                result.append(token)
    return result

def convertir_lista_oracion(lista_palabras):

    oracion = " ".join(lista_palabras)  # Unir las palabras con espacios
    return oracion





