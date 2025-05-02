from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import DATABASE_URL

Base = declarative_base()

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Translation(Base):
    __tablename__ = "translations"

    id = Column(Integer, primary_key=True, index=True)
    english = Column(String, nullable=False)
    german = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint("english", "german", name="uq_english_german"),
    )

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    english = Column(String, nullable=False)
    german = Column(String, nullable=False)

class Grammar(Base):
    __tablename__ = "grammar"

    id = Column(Integer, primary_key=True, index=True)
    german = Column(String, unique=True, nullable=False)
    grammar_explanations = Column(String, nullable=False)

class ReadingMetaData(Base):
    __tablename__ = "reading_metadata"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(String, nullable=False)
    topic = Column(String, nullable=False)

class ListeningMetaData(Base):
    __tablename__ = "listening_metadata"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(String, nullable=False)
    topic = Column(String, nullable=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)