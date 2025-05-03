from .prompt import get_listening_task_evaluation_prompt
from services.models import gemini_model
from .utils import extract_json_content_from_llm_response

def evaluate_listening_answers(topic, article, questions_and_answers, user_answers):
    """
    Evaluates user-submitted answers for a listening task using a language model.

    Constructs a prompt containing the topic, article, correct questions and answers, and the user's answers,
    then sends it to a language model to generate evaluation feedback and scores. The response is parsed
    to extract structured JSON data.

    Parameters
    -----------
    topic : str
        The topic of the listening exercise.
    article : str
        The main text or transcript related to the listening task.
    questions_and_answers : str
        A JSON or structured string of correct questions and their corresponding answers.
    user_answers : str
        A JSON or structured string containing the user's submitted answers.

    Returns
    --------
    dict
        A dictionary containing the evaluation results, including scores and explanations.
    """
    prompt = get_listening_task_evaluation_prompt(
        topic=topic,
        article=article,
        questions_and_answers=questions_and_answers,
        user_answers=user_answers
    )
    explanations_and_scores = gemini_model.generate_content(prompt).text
    explanations_and_scores_json = extract_json_content_from_llm_response(explanations_and_scores)
    return explanations_and_scores_json
