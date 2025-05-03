from sqlalchemy.orm import Session
from .models import Translation, Conversation, Grammar, ListeningMetaData, ReadingMetaData, WritingMetaData
from schemas.translation import TranslationModel
from schemas.conversation import  ConversationModel
from schemas.grammar import  GrammarModel
from schemas.metadata import ReadingMetaDataModel, ListeningMetaDataModel, WritingMetaDataModel


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

def save_reading_metadata(db: Session, reading_metadata_data: ReadingMetaDataModel):

    existing_reading_metadata = db.query(ReadingMetaData).filter_by(
        level=reading_metadata_data.level,
        topic=reading_metadata_data.topic
    ).first()

    if existing_reading_metadata:
        return existing_reading_metadata
    
    reading_metadata = ReadingMetaData(
        level=reading_metadata_data.level,
        topic=reading_metadata_data.topic
    )

    db.add(reading_metadata)
    db.commit()
    db.refresh(reading_metadata)
    return reading_metadata

def save_listening_metadata(db: Session, listening_metadata_data: ListeningMetaDataModel):

    existing_listening_metadata = db.query(ListeningMetaData).filter_by(
        level=listening_metadata_data.level,
        topic=listening_metadata_data.topic
    ).first()

    if existing_listening_metadata:
        return existing_listening_metadata
    
    listening_metadata = ListeningMetaData(
        level=listening_metadata_data.level,
        topic=listening_metadata_data.topic
    )

    db.add(listening_metadata)
    db.commit()
    db.refresh(listening_metadata)
    return listening_metadata

def save_writing_metadata_and_content(db: Session, metadata: WritingMetaDataModel):
    existing = db.query(WritingMetaData).filter_by(
        level=metadata.level,
        topic=metadata.topic,
        content=metadata.content
    ).first()
    if existing:
        return existing
    new_meta = WritingMetaData(level=metadata.level, topic=metadata.topic, content = metadata.content)
    db.add(new_meta)
    db.commit()
    db.refresh(new_meta)
    return new_meta