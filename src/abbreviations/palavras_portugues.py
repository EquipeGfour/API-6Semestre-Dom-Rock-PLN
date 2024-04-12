import pandas as pd
import re

# Carregando o conjunto de dados
dataset_types = {
    "submission_date": str,
    "reviewer_id": str,
    "product_id": str,
    "product_name": str,
    "product_brand": str,
    "site_category_lv1": str,
    "site_category_lv2": str,
    "review_title": str,
    "overall_rating": int,
    "recommend_to_a_friend": str,
    "review_text": str,
    "reviewer_birth_year": float,
    "reviewer_gender": str,
    "reviewer_state": str
}

# Carregando o arquivo CSV
dataset = pd.read_csv("B2W-Reviews01.csv", delimiter=",", dtype=dataset_types)

# Função para encontrar potenciais abreviaturas, siglas e palavras incorretas
def find_potential_abbreviations(text):
    # Expressão regular para encontrar palavras que podem ser abreviaturas, siglas ou palavras incorretas
    potential_abbr_pattern = r'\b(?![0-9])\w{1,3}\b'  # Considera palavras com até 3 letras como potenciais abreviações ou siglas
    # Encontrar todas as ocorrências
    potential_abbr_words = re.findall(potential_abbr_pattern, str(text), flags=re.IGNORECASE)
    return potential_abbr_words

# Inicializar contador
word_count = {}

# Iterar sobre as revisões
for review in dataset["review_text"]:
    # Encontrar potenciais abreviaturas, siglas e palavras incorretas
    potential_abbr_words = find_potential_abbreviations(review)
    # Contar ocorrências
    for word in potential_abbr_words:
        if word.lower() in word_count:
            word_count[word.lower()] += 1
        else:
            word_count[word.lower()] = 1

# Imprimir contagem de palavras
for word, count in sorted(word_count.items(), key=lambda x: x[1], reverse=True):
    try:
        print(f"{word}: {count}")
    except UnicodeEncodeError:
        print(f"{word.encode('utf-8')}: {count}")
