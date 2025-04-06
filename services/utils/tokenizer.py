import nltk
from nltk.tokenize import sent_tokenize

def split_sentences(sentence):

    # For first download
    nltk.download('punkt_tab')

    return sent_tokenize(sentence)