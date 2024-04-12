import unicodedata
import re
import nltk
from nltk.corpus import mac_morpho

# Remove acentos
def remove_accents(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return text

# Mapa de expansão de abreviações e contrações
MAP = {
    'RCB': 'relação custo-benefício',
    'nda': 'nada',
    "d'água": 'de água' 
}

# Expande abreviações e contrações
def expand_abbreviations_and_contractions(text, contraction_mapping):
    contractions_pattern = re.compile('({})'.format('|'.join(contraction_mapping.keys())), flags=re.IGNORECASE|re.DOTALL)
    def expand_match(contraction):
        match = contraction.group(0)
        first_char = match[0]
        expanded_contraction = contraction_mapping.get(match)\
                                if contraction_mapping.get(match)\
                                else contraction_mapping.get(match.lower())                       
        expanded_contraction = first_char+expanded_contraction[1:]
        return expanded_contraction
        
    expanded_text = contractions_pattern.sub(expand_match, text)
    expanded_text = re.sub("'", "", expanded_text)
    return expanded_text

# Remove caracteres repetidos em palavras
def remove_repeated_characters(token):
    repeat_pattern = re.compile(r'(\w*)(\w)\2(\w*)')
    match_substitution = r'\1\2\3'
    def replace(old_word):
        if old_word in mac_morpho.words():
            return old_word
        new_word = repeat_pattern.sub(match_substitution, old_word)
        return replace(new_word) if new_word != old_word else new_word
            
    correct_tokens = replace(token)
    return correct_tokens

# Função que processa um texto completo
def process_text(text):
    text_wo_accents = remove_accents(text)
    text_wo_abbr_and_contr = expand_abbreviations_and_contractions(text_wo_accents, MAP)
    processed_text = " ".join([remove_repeated_characters(word) for word in nltk.word_tokenize(text_wo_abbr_and_contr)])
    return processed_text
