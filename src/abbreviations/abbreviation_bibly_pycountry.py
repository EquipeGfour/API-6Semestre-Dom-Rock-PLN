import unicodedata
import spacy
import pandas as pd

# Carregar modelo de língua portuguesa
nlp = spacy.load("pt_core_news_sm")

# Função para remover acentos
def remove_accents(text):
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')

# Função para corrigir ortografia usando spaCy
def correct_spelling(text):
    doc = nlp(text)
    corrected_text = " ".join(token.lemma_ for token in doc)
    return corrected_text

# Carregar o CSV
def load_dataset(filename):
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
    dataset = pd.read_csv(filename, delimiter=",", dtype=dataset_types)
    return dataset

# Processamento do texto das reviews
def process_reviews(reviews):
    processed_reviews = []
    for review in reviews:
        # Remover acentos
        review = remove_accents(review)
        # Corrigir ortografia
        review = correct_spelling(review)
        processed_reviews.append(review)
    return processed_reviews

# Carregar os dados
dataset = load_dataset("B2W-Reviews01.csv")
train_data = dataset[-100:].dropna()
reviews = train_data["review_text"].tolist()

# Processar e exibir as reviews processadas
processed_reviews = process_reviews(reviews)
for review in processed_reviews:
    print(review)