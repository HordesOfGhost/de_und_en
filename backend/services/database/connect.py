import sqlite3
from dotenv import load_dotenv
import os
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    '''
        Connect to SQLITE database
    '''
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row 
    return conn
