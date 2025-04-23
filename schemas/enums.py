from enum import Enum

class TableName(str, Enum):
    conversations = "conversations"
    translations = "translations"