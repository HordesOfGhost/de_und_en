from services.models import model, tokenizer, device
from services.utils import split_sentences

def convert_to_de(input_text):

    sentences = split_sentences(input_text)

    translated_sentences = " "

    for sentence in sentences:
        inputs = tokenizer(f"<2de> {sentence}", return_tensors="pt")
        inputs = {k: v.to(device) for k, v in inputs.items()}

        # Generate output
        outputs = model.generate(**inputs)

        # Decode
        decoded_sentence = tokenizer.batch_decode(outputs, skip_special_tokens=True)

        translated_sentences += " " + decoded_sentence[0]
    
    return translated_sentences