from metodos import *
import csv
import pickle
from transformers import AutoTokenizer


if __name__ == "__main__":
    
    # Cargar modelo para la clasificacion
    model = pickle.load(open("E:\MIGUEL\Estudio\Hotel_Nacional\Model\model.pkl", "rb"))
    tokenizer = AutoTokenizer.from_pretrained("E:\MIGUEL\Estudio\Hotel_Nacional\Tokenaizer/")

    # Nombres de las columnas de archivo csv
    columnas = ["Opinion", "Oracion", "Aspecto","Segmento","Polaridad"]

    # Crear el archivo CSV con encabezado vacío
    with open("datos_salida.csv", "w", newline="") as archivo_csv:
        escritor_csv = csv.writer(archivo_csv, delimiter=";")
        escritor_csv.writerow(columnas)  # Escribir solo el encabezado

    #Cargar archivo csv con las opiniones
    ruta_archivo = "E:\MIGUEL\Estudio\Tesis\Sentiment_Analisis\Aspect\opiniones.csv" 

    #Cargar lista de palabras claves
    palabras_clave = ["hotel","guía","habitación","habitacion", "desayunos","comida","servicio","tour","piscina","personal","baño"] 

    # Procesar el archivo CSV [Devuelve lista de opiniones]
    opiniones = procesar_archivo(ruta_archivo)

    #Buscar opiniones relevantes [Opiniones donde exista algun aspecto]
    opiniones_relevantes = extraer_opiniones_relevantes(opiniones,palabras_clave)

    # LLenar el archivo de salida con todas sus columnas
    llenar_archivo_salida(model,tokenizer,opiniones_relevantes,palabras_clave)


    print("Fin del Proceso")