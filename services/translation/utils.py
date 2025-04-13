from services.models import madlad_model, madlad_tokenizer, device
from services.utils import split_sentences
import re

def translate_lng(input_text, target_language):
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


def add_newline_before_speaker(input_text: str) -> str:
    # Add two newlines before each speaker's name followed by a colon
    formatted_text = re.sub(r'(\b\w+:)', r'\n\n\1', input_text)

    # If the text starts with a newline, remove it to prevent unwanted leading newline
    if formatted_text.startswith("\n\n"):
        formatted_text = formatted_text[2:]
    
    return formatted_text
