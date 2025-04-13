from sqlalchemy.orm import Session
from .models import Translation, Conversation
from .schemas import TranslationModel, ConversationModel

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
