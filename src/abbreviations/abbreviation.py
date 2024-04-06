from spellchecker import SpellChecker
import unicodedata
import re
import sys

# Função para remover acentos
def remove_accents(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return text


# Mapeamento de contrações e abreviações
MAP = {
    'LTDA': 'limitada',
    'nda': 'nada',
    'mto':'muito',
    'vc': 'voce',
    'tv': 'televisao',
}

# Função para expandir contrações e abreviações
def expand_abbreviations_and_contractions(text, contraction_mapping):
    for key, value in contraction_mapping.items():
        text = re.sub(r'\b' + re.escape(key) + r'\b', value, text)
    return text

# Função para expandir casos especiais
def expand_special_cases(text):
    return text.replace("d'agua", "de agua")

# Função para remover caracteres especiais
def remove_special_characters(token):
    return re.sub(r'[^\w\s]', '', token)

# Função para corrigir ortografia usando pyspellchecker
def correct_spelling(word):
    spell = SpellChecker(language='pt')
    # Verifique se a palavra está correta
    corrected_word = spell.correction(word)
    if corrected_word != word:
        # Se a palavra foi corrigida, retorne a correção
        return corrected_word
    else:
        # Se a palavra estava correta ou não pôde ser corrigida, retorne a palavra original
        return word

# Texto de exemplo
sample_text = ("produto mto bom, com essa garrafinha vc pode até servir água pro megazord"
               " To pensando em vender minha tv pra comprar 1 garrafa dessa. RECOMENDO")

# Corrigindo a palavra 'friiio' no texto original
sample_text_corrected = sample_text.replace("friiio", "frios")

sample_text_wo_accents = remove_accents(sample_text_corrected)
sample_text_wo_abbr_and_contr = expand_abbreviations_and_contractions(sample_text_wo_accents, MAP)
sample_text_wo_special_cases = expand_special_cases(sample_text_wo_abbr_and_contr)

# Aplicando correção ortográfica no texto
words = sample_text_wo_special_cases.split()
corrected_text = ' '.join(correct_spelling(word) or word for word in words if word.strip())

# Exibindo o texto corrigido
print("Texto corrigido:")
sys.stdout.buffer.write(corrected_text.encode('utf-8'))
print()

# Corrigindo palavra específica
word = "friiio"
corrected_word = correct_spelling(word) or word
print("Palavra corrigida:", corrected_word)
