from pydantic import BaseModel

class GrammarModel(BaseModel):
    english: str
    german: str
    grammar_explanations: str

    class Config:
        from_attributes = True
