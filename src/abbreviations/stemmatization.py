from pandas import read_csv
from nltk.stem import SnowballStemmer
from nltk.tokenize import ToktokTokenizer

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

tokenizer = ToktokTokenizer()
stemmer = SnowballStemmer(language='portuguese')

stemmed_reviews = []

for review in reviews:
    tokens = tokenizer.tokenize(review)
    stemmed_tokens = [stemmer.stem(token) for token in tokens]
    stemmed_review = ' '.join(stemmed_tokens)
    stemmed_reviews.append(stemmed_review)

for review in stemmed_reviews:
    print(review)
