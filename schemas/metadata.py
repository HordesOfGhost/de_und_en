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

