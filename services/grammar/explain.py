from .prompt import prompt_template_for_grammar_explanation_of_german_sentences
from .utils import extract_raw_html
from services.models import gemini_model
from schemas.grammar import GrammarModel
from services.db.crud_for_services import save_grammar_explanation
from sqlalchemy.orm import Session

def explain_and_save_grammar_for_german_sentences(german_sentences: str, db: Session):
    prompt = prompt_template_for_grammar_explanation_of_german_sentences.format(german_sentences=german_sentences)
    grammar_explanations = gemini_model.generate_content(prompt).text
    grammar_explanations = extract_raw_html(grammar_explanations)

    grammar_explanations_data = GrammarModel(
        german=german_sentences,
        grammar_explanations=grammar_explanations
    )

    saved_grammar_explanations = save_grammar_explanation(db, grammar_explanations_data)
    return grammar_explanations, saved_grammar_explanations.id
