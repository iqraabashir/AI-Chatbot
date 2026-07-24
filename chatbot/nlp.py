from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from spellchecker import SpellChecker

stop_words = set(stopwords.words("english"))
stemmer = PorterStemmer()
spell = SpellChecker()

def preprocess_text(text):
    text = text.lower()
    text = correct_spelling(text)
    tokens = word_tokenize(text)
    filtered_words = []

    for word in tokens:
        if word.isalnum() and word not in stop_words:
            filtered_words.append(stemmer.stem(word))
    return filtered_words

def correct_spelling(text):
    corrected_words = []
    words = text.split()
    for word in words:
        corrected_word = spell.correction(word)
        corrected_words.append(corrected_word)
    return " ".join(corrected_words)