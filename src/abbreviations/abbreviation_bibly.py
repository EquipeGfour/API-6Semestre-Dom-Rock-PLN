from pandas import read_csv
import unicodedata
import re
from spellchecker import SpellChecker
import contractions

# Carregando o conjunto de dados
dataset_types = {
    "submission_date": str,
    "reviewer_id":str,
    "product_id": str,
    "product_name": str,
    "product_brand": str,
    "site_category_lv1":str,
    "site_category_lv2":str, 
    "review_title": str,
    "overall_rating": int,
    "recommend_to_a_friend": str,
    "review_text": str,
    "reviewer_birth_year": float,
    "reviewer_gender": str,
    "reviewer_state": str
}

dataset = read_csv("B2W-Reviews01.csv", delimiter=",", dtype=dataset_types)
train_data = dataset[-100:].dropna()
reviews = train_data["review_text"].tolist()

# Função para remover acentos
def remove_accents(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return text

# Função para remover caracteres especiais
def remove_special_characters(token):
    return re.sub(r'[^\w\s]', '', token)

# Função para corrigir ortografia usando pyspellchecker
def correct_spelling(word):
    spell = SpellChecker(language='pt')
    corrected_word = spell.correction(word)
    if corrected_word != word:
        return corrected_word
    else:
        return word

# Processamento do texto das reviews
processed_reviews = []
for review in reviews:
    # Remover acentos
    review = remove_accents(review)
    # Expandir contrações
    review = contractions.fix(review)
    # Remover caracteres especiais
    review = remove_special_characters(review)
    # Corrigir ortografia
    words = review.split()
    corrected_review = ' '.join(correct_spelling(word) or word for word in words if word.strip())
    processed_reviews.append(corrected_review)

# Exibindo as reviews processadas
for review in processed_reviews:
    print(review)
