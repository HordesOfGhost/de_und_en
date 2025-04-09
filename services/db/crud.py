from sqlalchemy.orm import Session
from .models import Translation
from .schemas import TranslationModel

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
