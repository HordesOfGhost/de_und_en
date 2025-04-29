from services.models import gemini_model
from .prompt import prompt_template_for_conversation_generation
from services.translation import translate_conversation_and_save_with_gemini
from sqlalchemy.orm import Session

def generate_conversation_translate_and_save(topic : str, db : Session):
    prompt = prompt_template_for_conversation_generation.format(topic)
    english_conversation = gemini_model.generate_content(prompt).text
    english_conversation = english_conversation.replace("*","")
    german_conversation, saved_conversation = translate_conversation_and_save_with_gemini(english_conversation, db)

    return english_conversation, german_conversation, saved_conversation.id
