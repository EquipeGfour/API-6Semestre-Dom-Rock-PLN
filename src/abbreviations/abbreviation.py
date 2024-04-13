from pandas import read_csv
import unicodedata
import re
from spellchecker import SpellChecker
import contractions

# Dicionário de expansão de siglas, abreviaturas e gírias
expansions = {
    "obs": "observacao",
    "obg": "obrigado",
    "blz": "beleza",
    "mto": "muito",
    "mta": "muita",
    "mt": "muito",
    "mts": "muitos",
    "vc": "voce",
    "vcs": "voces",
    "tv": "televisao",
    "tvs": "televisoes",
    "pq": "porque",
    "oq": "o que",
    "qd": "quando",
    "q": "que",
    "ñ": "nao",
    "td": "tudo",
    "tds": "tudos",
    "tb": "tambem",
    "tbm": "tambem",
    "etc": "e outras coisas",
    "hj": "hoje",
    "app": "aplicativo",
    "SAC": "servico de Atendimento ao Consumidor",
    "LTDA": "limitada",
    "qdo": "quando",
    "msm": "mesmo",
    "net": "internet",
    "min": "minuto",
    "cel": "celular",
    "cell": "celular",
    "qto": "quanto",
    "qq": "qualquer",
    "not": "notebook",
    "hrs": "horas",
    "hr": "horas",
    "msg": "mensagem",
    "agr": "agora",
    "tdo": "tudo",
    "ngm": "ninguem",
    "vdd": "verdade",
    "vlw": "valeu"
}

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

# Função para remover palavras seguidas de números e números seguidos de palavras
def remove_words_with_numbers(token):
    return re.sub(r'\b(?:\w*\d\w*|\d\w*\d)\b', '', token)

# Função para corrigir ortografia usando pyspellchecker
def correct_spelling(word):
    spell = SpellChecker(language='pt')
    corrected_word = spell.correction(word)
    if corrected_word != word:
        return corrected_word
    else:
        return word

# Função para expandir siglas, abreviaturas e gírias
def expand_abbreviations(text):
    words = text.split()
    expanded_words = [expansions[word] if word in expansions else word for word in words]
    return ' '.join(expanded_words)

# Processamento do texto das reviews
processed_reviews = []
for review in reviews:
    # Remover acentos
    review = remove_accents(review)
    # Expandir contrações
    review = contractions.fix(review)
    # Expandir siglas, abreviaturas e gírias
    review = expand_abbreviations(review)
    # Remover palavras seguidas de números e números seguidos de palavras
    review = remove_words_with_numbers(review)
    # Corrigir ortografia
    words = review.split()
    corrected_review = ' '.join(correct_spelling(word) or word for word in words if word.strip())
    processed_reviews.append(corrected_review)

# Exibindo as reviews processadas
for review in processed_reviews:
    print(review)
