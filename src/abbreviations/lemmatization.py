import spacy
from pandas import read_csv

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

dataset = read_csv("B2W-Reviews01.csv", delimiter=",", dtype=dataset_types)
train_data = dataset[-100:].dropna()
reviews = train_data["review_text"].tolist()

# Inicializando o modelo Spacy
spacy_nlp = spacy.load('pt_core_news_sm', disable=['parser', 'ner'])

# Função para lematizar um texto usando Spacy
def lemmatize_spacy(text):
    return [token.lemma_ for token in spacy_nlp(text)]

# Lematizar as avaliações usando Spacy
lemmatized_reviews_spacy = [lemmatize_spacy(review) for review in reviews]

# Exemplo de saída
print("Texto lemmatizado:")
print(lemmatized_reviews_spacy[0])
