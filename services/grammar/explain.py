from .prompt import get_prompt_for_grammar_explanation_of_german_sentences
from .utils import extract_raw_html
from services.models import gemini_model
from schemas.grammar import GrammarModel
from services.db.crud_for_services import save_grammar_explanation
from sqlalchemy.orm import Session

def explain_and_save_grammar_for_german_sentences(german_sentences: str, db: Session):
    """
    Generate a grammar explanation for the provided German sentences and save it to the database.

    Parameters
    -----------
    german_sentences: str
        The German sentences for which the grammar explanation will be generated.
    
    db: Session
        The database session used to interact with the database.

    Returns
    --------
    grammar_explanations: str
        The generated grammar explanation for the given German sentences.

    saved_grammar_explanation_id: int
        The ID of the saved grammar explanation in the database.

    """
    prompt = get_prompt_for_grammar_explanation_of_german_sentences(german_sentences=german_sentences)
    grammar_explanations = gemini_model.generate_content(prompt).text
    grammar_explanations = extract_raw_html(grammar_explanations)

    grammar_explanations_data = GrammarModel(
        german=german_sentences,
        grammar_explanations=grammar_explanations
    )

    saved_grammar_explanations = save_grammar_explanation(db, grammar_explanations_data)
    return grammar_explanations, saved_grammar_explanations.id
