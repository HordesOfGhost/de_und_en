from .prompt import get_reading_task_evaluation_prompt
from services.models import gemini_model
from .utils import extract_json_content_from_llm_response

def evaluate_reading_answers(topic: str, article: str, questions_and_answers: list, user_answers: list):
    """
    Evaluates user answers for a reading comprehension task using an LLM.

    Constructs a prompt using the topic, article, original questions and answers, and user responses.
    Sends the prompt to the Gemini model and parses the JSON-formatted explanation and score output.

    Parameters
    -----------
    topic : str
        The topic of the reading passage.
    article : str
        The content of the reading article.
    questions_and_answers : list[dict]
        List of dictionaries containing original questions and correct answers.
    user_answers : list[str]
        List of user's answers corresponding to the questions.

    Returns
    --------
    dict
        A dictionary containing explanations and evaluation scores for each answer.
    """

    prompt = get_reading_task_evaluation_prompt(topic=topic, article=article, questions_and_answers=questions_and_answers, user_answers=user_answers)
    explanations_and_scores = gemini_model.generate_content(prompt).text
    explanations_and_scores_json = extract_json_content_from_llm_response(explanations_and_scores)
    return explanations_and_scores_json
