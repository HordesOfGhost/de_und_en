from pydantic import BaseModel

class TranslationModel(BaseModel):
    english: str
    german: str

    class Config:
        orm_mode = True 
