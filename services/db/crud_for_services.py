from sqlalchemy.orm import Session
from .models import Translation, Conversation, Grammar
from schemas.translation import TranslationModel
from schemas.conversation import  ConversationModel
from schemas.grammar import  GrammarModel

def save_translation(db: Session, translation_data: TranslationModel):
    
    # Check if translation exists
    existing_translation = db.query(Translation).filter_by(
        english=translation_data.english,
        german=translation_data.german
    ).first()

    if existing_translation:
        return existing_translation

    # Else add translation
    translation = Translation(
        english=translation_data.english,
        german=translation_data.german
    )

    db.add(translation)
    db.commit()
    db.refresh(translation)
    return translation

def save_conversation(db: Session, conversation_data: ConversationModel):
    conversation = Conversation(
        english=conversation_data.english,
        german=conversation_data.german
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation

def save_grammar_explanation(db: Session, grammar_explanations_data: GrammarModel):

    existing_grammar_explanation = db.query(Grammar).filter_by(
        german=grammar_explanations_data.german,
        grammar_explanations=grammar_explanations_data.grammar_explanations
    ).first()

    if existing_grammar_explanation:
        return existing_grammar_explanation
    
    grammar_explanation = Grammar(
        german=grammar_explanations_data.german,
        grammar_explanations=grammar_explanations_data.grammar_explanations
    )

    db.add(grammar_explanation)
    db.commit()
    db.refresh(grammar_explanation)
    return grammar_explanation
