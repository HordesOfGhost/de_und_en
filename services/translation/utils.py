from services.models import madlad_model, madlad_tokenizer, device
from services.models import gemini_model
from .prompt import get_prompt_for_language_translation
from services.utils import split_sentences
import re

# Legacy with madlad
def translate_lng_with_madlad(input_text, target_language):
    """
    Translates input text from one language to another using the Madlad translation model.

    The function splits the input text into sentences, then uses the Madlad model to 
    translate each sentence. The sentences are combined into a single translated text.

    Parameters
    -----------
    input_text : str
        The text to be translated.
    target_language : str
        The target language for translation, such as "de" for German or "en" for English.

    Returns
    --------
    str
        The translated text.
    """

    sentences = split_sentences(input_text)
    translated_sentences = " "

    for sentence in sentences:
        inputs = madlad_tokenizer(f"<{target_language}> {sentence}", 
                    return_tensors="pt", 
                    max_length=1024, 
                    truncation=True, 
                    padding="longest")
        
        inputs = {k: v.to(device) for k, v in inputs.items()}

        # Generate output
        outputs = madlad_model.generate(**inputs,
            max_length=1024,
            num_beams=4,
            early_stopping=True
        )

        # Decode
        decoded_sentence = madlad_tokenizer.batch_decode(outputs, skip_special_tokens=True)
        translated_sentences += " " + decoded_sentence[0]
    
    return translated_sentences.strip()

def translate_lng_with_gemini(input_text, target_language):
    """
    Translates input text from one language to another using the Gemini translation model.

    The function constructs a prompt for the Gemini model to translate the input text 
    between English and German based on the target language specified.

    Parameters
    -----------
    input_text : str
        The text to be translated.
    target_language : str
        The target language for translation, either "de" for German or "en" for English.

    Returns
    --------
    str
        The translated text.
    """

    # sentences = split_sentences(input_text)
    # translated_sentences = " "

    if target_language=="de":
        prompt = get_prompt_for_language_translation(lng1='English',lng2='German', text = input_text)

        translated_sentences = gemini_model.generate_content(prompt).text
    elif target_language=="en":
        prompt = get_prompt_for_language_translation(lng1='German',lng2='English', text = input_text)

        translated_sentences = gemini_model.generate_content(prompt).text
    return translated_sentences.strip()


def add_newline_before_speaker(input_text: str) -> str:
    """
    Adds two newlines before each speaker's name followed by a colon in the input text.

    This function formats the input text by adding spacing before each speaker's name
    to make the dialogue more readable, especially in transcription scenarios.

    Parameters
    -----------
    input_text : str
        The text to be formatted, typically containing speaker names and their dialogue.

    Returns
    --------
    str
        The formatted text with newlines added before each speaker's name.
    """

    # Add two newlines before each speaker's name followed by a colon
    formatted_text = re.sub(r'(\b\w+:)', r'\n\n\1', input_text)

    # If the text starts with a newline, remove it to prevent unwanted leading newline
    if formatted_text.startswith("\n\n"):
        formatted_text = formatted_text[2:]
    
    return formatted_text
