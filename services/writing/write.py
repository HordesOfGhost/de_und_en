from services.models import gemini_model
from .prompt import get_prompt_for_generating_writing_content
from sqlalchemy.orm import Session
from .utils import extract_json_content_from_llm_response
from schemas.metadata import WritingMetaDataModel
# from services.db.crud_for_services import save_writing_metadata

def generate_writing_topic(level: str, db:Session):
    prompt = get_prompt_for_generating_writing_content(level, db)
    response = gemini_model.generate_content(prompt).text
    print(response)
    json_response = extract_json_content_from_llm_response(response)
    print(json_response)
    return json_response