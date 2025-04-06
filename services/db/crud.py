from sqlalchemy.orm import Session
from .models import Translation
from .schemas import TranslationModel

def save_translation(db: Session, translation_data: TranslationModel):
    translation = Translation(english=translation_data.english, german=translation_data.german)
    db.add(translation)
    db.commit()
    db.refresh(translation)
    return translation