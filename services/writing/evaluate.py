from .prompt import get_writing_evaluation_prompt
from services.models import gemini_model
from .utils import extract_json_content_from_llm_response
from schemas.metadata import WritingMetaDataModel
from services.db.crud_for_services import save_writing_metadata_and_content

def evaluate_writing_answers(topic, level, content,db):
    prompt = get_writing_evaluation_prompt(topic=topic, level=level, content=content)
    explanations_and_scores = gemini_model.generate_content(prompt).text
    explanations_and_scores_json = extract_json_content_from_llm_response(explanations_and_scores)
    save_meta_data = WritingMetaDataModel(topic=topic, level=level, content=content)
    save_writing_metadata_and_content(db,save_meta_data)
    return explanations_and_scores_json
