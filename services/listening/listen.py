from services.models import gemini_model
from .prompt import prompt_for_generating_listening_content
from sqlalchemy.orm import Session
from .utils import extract_json_content_from_llm_response

def generate_listening_content(level: str):
    prompt = prompt_for_generating_listening_content.format(level=level)
    response = gemini_model.generate_content(prompt).text
    json_response = extract_json_content_from_llm_response(response)
    return json_response