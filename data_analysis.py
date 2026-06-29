# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm

#leer archivo
df = pd.read_excel('/content/drive//Dataset tedic.xlsx')

# mostrar primeras filas y descripción estadística
df.head()
df.describe(include='all')

# Instalar NLTK, una librería muy
# usada para procesamiento de lenguaje natural.

import nltk
from nltk.corpus import stopwords

# Descargar stopwords en español para palabras vacías como la o el
nltk.download('stopwords')

# Cargar stopwords en una variable
spanish_stopwords = stopwords.words('spanish')

#Define vocabulario para lenguaje emocional, adjetivos excesivos y contenido violento
# Estas son listas seleccionadas basadas en patrones comunes del lenguaje mediático

emotional_vocab = {
    'orgullo', 'orgulloso', 'feliz', 'contento', 'triste', 'dolor', 'sufrimiento',
    'angustia', 'miedo', 'terror', 'pánico', 'esperanza', 'desesperación', 'ira',
    'rabia', 'furia', 'amor', 'odio', 'pasión', 'emoción', 'emocional', 'sentimiento',
    'plenamente', 'comprometido', 'dedicado', 'apasionado', 'desgarrador', 'conmovedor',
    'impactante', 'sorprendente', 'asombroso', 'increíble', 'maravilloso', 'terrible',
    'horrible', 'espantoso', 'dramático', 'trágico', 'catastrófico', 'desastroso'
}

excessive_adj = {
    'enorme', 'gigantesco', 'colosal', 'monumental', 'extraordinario', 'excepcional',
    'fantástico', 'magnífico', 'espléndido', 'sublime', 'perfecto', 'impecable',
    'inmaculado', 'radiante', 'deslumbrante', 'brillante', 'luminoso', 'resplandeciente',
    'hermoso', 'bellísimo', 'precioso', 'divino', 'celestial', 'paradisíaco',
    'infernal', 'diabólico', 'monstruoso', 'abominable', 'repugnante', 'asqueroso',
    'nauseabundo', 'detestable', 'execrable', 'abominable', 'pésimo', 'malísimo',
    'terrible', 'horroroso', 'espantoso', 'aterrador', 'terrorífico', 'escalofriante',
    'desgarrador', 'angustioso', 'desolador', 'devastador', 'arrasador', 'fulminante',
    'aplastante', 'abrumador', 'sofocante', 'opresivo', 'agobiante', 'asfixiante'
}

violent_vocab = {
    'violencia', 'violento', 'agresión', 'agresivo', 'ataque', 'atacar', 'golpe',
    'golpear', 'pelea', 'peleador', 'combate', 'batalla', 'guerra', 'conflicto',
    'enfrentamiento', 'choque', 'colisión', 'impacto', 'explosión', 'bomba',
    'arma', 'armado', 'disparo', 'bala', 'cuchillo', 'puñal', 'navaja',
    'muerte', 'muerto', 'matar', 'asesinato', 'asesino', 'homicidio', 'crimen',
    'criminal', 'delito', 'delincuente', 'robo', 'robar', 'asalto', 'asaltante',
    'secuestro', 'secuestrador', 'violación', 'violador', 'abuso', 'maltrato',
    'tortura', 'torturador', 'castigo', 'castigo corporal', 'represalia', 'venganza',
    'sangre', 'sangriento', 'herida', 'herido', 'lesión', 'lesionado', 'trauma',
    'traumático', 'pánico', 'pánico', 'terror', 'terrorismo', 'terrorista',
    'vuelco', 'accidente', 'choque', 'colisión', 'desastre', 'catástrofe',
    'destrucción', 'destruir', 'ruina', 'arruinar', 'devastación', 'devastar'
}

print("- Lenguaje emocional:", len(emotional_vocab), "palabras")
print("- Adjetivación excesiva:", len(excessive_adjectives), "palabras")
print("- Contenido violento:", len(violent_vocab), "palabras")

import re
from tqdm import tqdm

import unicodedata

#normalizar texto

def normalize_text(text):
    if pd.isna(text):
        return ""

    text = str(text).lower()

    text = ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )

    text = re.sub(r'\s+', ' ', text).strip()

    return text
# Función para verificar la presencia de vocabulario
def check_vocabulary(text, vocab_set):

    if not text:
        return False
    words = re.findall(r'\b\w+\b', text)
    return any(word in vocab_set for word in words)


# Función para contar coincidencias de vocabulario
def count_vocabulary_matches(text, vocab_set):
    if not text:
        return 0

    words = re.findall(r'\b\w+\b', text)
    return sum(1 for word in words if word in vocab_set)

# Función para analizar y calificar el contenido (escala 1-5)
def rate_content(text, emotional_vocab, excessive_adj, violent_vocab):
   
    if not text:
        return 1

    emotional_count = count_vocabulary_matches(text, emotional_vocab)
    adjective_count = count_vocabulary_matches(text, excessive_adj)
    violent_count = count_vocabulary_matches(text, violent_vocab)

    total_score = 0

    #Puntuación por lenguaje emocional
    if emotional_count > 0:
        total_score += min(emotional_count, 2)  # Máximo 2 puntos
    #Puntuación por adjetivos excesivos
    if adjective_count > 0:
        total_score += min(adjective_count, 2)  # Máximo 2 puntos
    # Puntuación por contenido violento (Aquí puse mayor peso)
    if violent_count > 0:
        total_score += min(violent_count * 1.5, 3)  # Máximo 3 puntos
    #Convertir a una  escala del  1 al 5
    rating = min(5, max(1, int(total_score) + 1))
    return rating

#Aquí identificamos qué categorías están presentes
def identify_categories(text, emotional_vocab, excessive_adj, violent_vocab):
    categories = []
    if check_vocabulary(text, emotional_vocab):
        categories.append("Lenguaje emocional")
    if check_vocabulary(text, excessive_adj):
        categories.append("Adjetivación excesiva")
    if check_vocabulary(text, violent_vocab):
        categories.append("Contenido violento")

    return ", ".join(categories) if categories else "Ninguno"

# Normalizar todos los captions
print("Normalizando captions...")
df['caption_normalized'] = df['caption'].apply(normalize_text)




# Crear las tres nuevas columnas
print("Analizando contenido...")
df['tiene_lenguaje_problematico'] = 'No'
df['nivel_intensidad'] = 1
df['categorias_identificadas'] = 'Ninguno'

for idx in tqdm(range(len(df)), desc="Procesando filas"):
    text = df['caption_normalized'].iloc[idx]

    # Columna 1: Sí/No si hay algún vocabulario presente
    has_any = (check_vocabulary(text, emotional_vocab) or
               check_vocabulary(text, excessive_adj) or
               check_vocabulary(text, violent_vocab))
    df.loc[idx, 'tiene_lenguaje_problematico'] = 'Sí' if has_any else 'No'

    # Columna 2: Calificación 1-5
    df.loc[idx, 'nivel_intensidad'] = rate_content(text, emotional_vocab, excessive_adj, violent_vocab)

    # Columna 3: Qué categorías aparecen
    df.loc[idx, 'categorias_identificadas'] = identify_categories(text, emotional_vocab, excessive_adj, violent_vocab)

print("Análisis completado")

# Guardar resultados
nombre_archivo = "Dataset_tedic_analizado.xlsx"
df.to_excel(nombre_archivo, index=False)

from google.colab import files
files.download(nombre_archivo)
