from services.models import gemini_model
from .prompt import prompt_template
from services.translation import translate_conversation_and_save
from sqlalchemy.orm import Session

def generate_conversation_translate_and_save(topic : str, db : Session):
    prompt = prompt_template.format(topic)
    english_conversation = gemini_model.generate_content(prompt).text
    german_conversation,_ = translate_conversation_and_save(english_conversation, db)

    return english_conversation, german_conversation
