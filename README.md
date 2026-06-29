# news-language-classifier
Data analysis script used to classify social media captions by emotional, sensational, and violent language patterns.
Script de análisis de datos utilizado para clasificar los textos de publicaciones en redes sociales según patrones de lenguaje emocional, sensacionalista y violento.

The information was scrapped with the programa name "Apify" first, because Instagram does not allow scrapping in a easy way!

##Methodology

The process includes:

Text normalization (lowercasing, removing accents, cleaning whitespace)

1) Rule-based matching against predefined vocabularies:
Emotional language
Excessive adjectives
Violence-related terms
Scoring system to estimate content intensity (scale 1–5)

2) The script generates three main columns:

tiene_lenguaje_problematico: indicates whether any target vocabulary is present
nivel_intensidad: score from 1 to 5 based on language intensity
categorias_identificadas: labels indicating detected language categories

##Tools Used in this analysis:
Python
pandas
re (regular expressions)
unicodedata
tqdm

# Findings

Posts related to violence generated the highest engagement, including comments, likes, and other interactions.

Author

Lía Barrios
