from nltk.tokenize import sent_tokenize
from nltk.data import find
from nltk import download

def split_sentences(sentence):
    """
    Splits a given sentence into individual sentences using NLTK's sentence tokenizer.

    This function checks if the required NLTK tokenizer data ('punkt') is available and 
    downloads it if not. Then, it tokenizes the input sentence into a list of sentences.

    Parameters
    -----------
    sentence : str
        A string representing the text to be split into sentences.

    Returns
    --------
    list of str
        A list containing the individual sentences that were tokenized from the input text.

    Example
    --------
    split_sentences("Hello world. This is an example.") 
    returns ['Hello world.', 'This is an example.']
    """
    
    try:
        find("tokenizers/punkt")
    except:
        download('punkt')

    return sent_tokenize(sentence)


def batch_sentences(sentences, batch_size=5):
    """
    Groups a list of sentences into batches of a specified size.

    This function takes a list of sentences and yields them in batches, where each batch is 
    a string of sentences joined together. The size of each batch is defined by the `batch_size` parameter.

    Parameters
    -----------
    sentences : list of str
        A list of sentences that need to be grouped into batches.
    batch_size : int, optional, default=5
        The number of sentences to include in each batch. If the list of sentences cannot be 
        evenly divided by the batch size, the final batch may contain fewer sentences.

    Returns
    --------
    generator
        A generator that yields batches of sentences, where each batch is a string of sentences.

    Example
    --------
    batch_sentences(['sentence1', 'sentence2', 'sentence3', 'sentence4', 'sentence5'], 2)
    returns:
    - 'sentence1 sentence2'
    - 'sentence3 sentence4'
    - 'sentence5'
    """
    
    for i in range(0, len(sentences), batch_size):
        yield ' '.join(sentences[i:i + batch_size])
