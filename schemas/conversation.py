from pydantic import BaseModel

class ConversationModel(BaseModel):
    english: str
    german: str

    class Config:
        from_attributes = True
