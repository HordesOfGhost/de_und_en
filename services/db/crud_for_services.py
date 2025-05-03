from sqlalchemy.orm import Session
from .models import Translation, Conversation, Grammar, ListeningMetaData, ReadingMetaData, WritingMetaData
from schemas.translation import TranslationModel
from schemas.conversation import ConversationModel
from schemas.grammar import GrammarModel
from schemas.metadata import ReadingMetaDataModel, ListeningMetaDataModel, WritingMetaDataModel
from .utils import save_if_not_exists

def save_translation(db: Session, translation_data: TranslationModel):
    """
    Save a translation record to the database if it doesn't already exist.
    
    Parameters
    -----------
    db: Session
        The SQLAlchemy session object.
    translation_data: TranslationModel
        The data for the translation to save.

    Returns
    --------
    Translation
        The saved or existing translation record.
    """
    return save_if_not_exists(
        db, Translation,
        {"english": translation_data.english, "german": translation_data.german},
        {"english": translation_data.english, "german": translation_data.german}
    )

def save_conversation(db: Session, conversation_data: ConversationModel):
    """
    Save a conversation record to the database if it doesn't already exist.

    Parameters:
    -----------
    db: Session
        The SQLAlchemy session object.
    conversation_data: ConversationModel
        The data for the conversation to save.

    Returns:
    --------
    Conversation
        The saved or existing conversation record.
    """
    return save_if_not_exists(
        db, Conversation,
        {"english": conversation_data.english, "german": conversation_data.german},
        {"english": conversation_data.english, "german": conversation_data.german}
    )

def save_grammar_explanation(db: Session, grammar_explanations_data: GrammarModel):
    """
    Save a grammar explanation record to the database if it doesn't already exist.

    Parameters:
    -----------
    db: Session
        The SQLAlchemy session object.
    grammar_explanations_data: GrammarModel
        The data for the grammar explanation to save.

    Returns:
    --------
    Grammar
        The saved or existing grammar explanation record.
    """
    return save_if_not_exists(
        db, Grammar,
        {"german": grammar_explanations_data.german, "grammar_explanations": grammar_explanations_data.grammar_explanations},
        {"german": grammar_explanations_data.german, "grammar_explanations": grammar_explanations_data.grammar_explanations}
    )

def save_reading_metadata(db: Session, reading_metadata_data: ReadingMetaDataModel):
    """
    Save reading metadata to the database if it doesn't already exist.

    Parameters
    -----------
    db: Session
        The SQLAlchemy session object.
    reading_metadata_data: ReadingMetaDataModel
        The data for the reading metadata to save.

    Returns
    --------
    ReadingMetaData
        The saved or existing reading metadata record.
    """
    return save_if_not_exists(
        db, ReadingMetaData,
        {"level": reading_metadata_data.level, "topic": reading_metadata_data.topic},
        {"level": reading_metadata_data.level, "topic": reading_metadata_data.topic}
    )

def save_listening_metadata(db: Session, listening_metadata_data: ListeningMetaDataModel):
    """
    Save listening metadata to the database if it doesn't already exist.

    Parameters
    -----------
    db: Session
        The SQLAlchemy session object.
    listening_metadata_data: ListeningMetaDataModel
        The data for the listening metadata to save.

    Returns
    --------
    ListeningMetaData
        The saved or existing listening metadata record.
    """
    return save_if_not_exists(
        db, ListeningMetaData,
        {"level": listening_metadata_data.level, "topic": listening_metadata_data.topic},
        {"level": listening_metadata_data.level, "topic": listening_metadata_data.topic}
    )

def save_writing_metadata_and_content(db: Session, metadata: WritingMetaDataModel):
    """
    Save writing metadata and content to the database if it doesn't already exist.

    Parameters
    -----------
    db: Session
        The SQLAlchemy session object.
    metadata: WritingMetaDataModel
        The data for the writing metadata to save.

    Returns
    --------
    WritingMetaData
        The saved or existing writing metadata record.
    """
    return save_if_not_exists(
        db, WritingMetaData,
        {"level": metadata.level, "topic": metadata.topic, "content": metadata.content},
        {"level": metadata.level, "topic": metadata.topic, "content": metadata.content}
    )