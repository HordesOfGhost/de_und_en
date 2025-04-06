from nltk.tokenize import sent_tokenize
from nltk.data import find
from nltk import download

def split_sentences(sentence):

    try:
        find("tokenizer/punkt")
    except:
        download('punkt')

    return sent_tokenize(sentence)