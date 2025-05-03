from nltk.tokenize import sent_tokenize
from nltk.data import find
from nltk import download

def split_sentences(sentence):

    try:
        find("tokenizers/punkt")
    except:
        download('punkt')

    return sent_tokenize(sentence)

def batch_sentences(sentences, batch_size=5):
    for i in range(0, len(sentences), batch_size):
        yield ' '.join(sentences[i:i + batch_size])
