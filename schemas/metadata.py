from pydantic import BaseModel

class ReadingMetaDataModel(BaseModel):
    level: str
    topic: str

    class Config:
        from_attributes = True

class ListeningMetaDataModel(BaseModel):
    level: str
    topic: str

    class Config:
        from_attributes = True

class WritingMetaDataModel(BaseModel):
    level: str
    topic: str
    content: str
    
    class Config:
        from_attributes = True

