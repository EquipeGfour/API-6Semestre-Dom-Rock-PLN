import spacy
import pycountry

# Carregar modelo de linguagem do spacy
nlp = spacy.load("en_core_web_sm")

def expand_abbreviations(text):
    doc = nlp(text)
    expanded_text = []
    for token in doc:
        # Expandir abreviações de países
        if token.text.upper() in pycountry.countries:
            expanded_text.append(pycountry.countries.get(alpha_2=token.text.upper()).name)
        # Expandir outras abreviações com o mesmo texto
        elif token.text.upper() in (ent.text.upper() for ent in doc.ents):
            expanded_text.append(token.text)
        # Manter outras palavras inalteradas
        else:
            expanded_text.append(token.text)
    return " ".join(expanded_text)

# Exemplo de uso
texto = "A empresa Ltda foi fundada em 1990 e se tornou uma S/A em 2005. Ela está localizada nos EUA."
texto_expandido = expand_abbreviations(texto)
print(texto_expandido)