from .prompt import get_listening_task_evaluation_prompt
from services.models import gemini_model
from .utils import extract_json_content_from_llm_response

def evaluate_listening_answers(topic, article, questions_and_answers, user_answers):
    prompt = get_listening_task_evaluation_prompt(topic=topic, article=article, questions_and_answers=questions_and_answers, user_answers=user_answers)
    explanations_and_scores = gemini_model.generate_content(prompt).text
    explanations_and_scores_json = extract_json_content_from_llm_response(explanations_and_scores)
    return explanations_and_scores_json
