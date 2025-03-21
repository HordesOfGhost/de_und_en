import sqlite3
from services.database import get_db_connection
from .auth import hash_password

def register_user(username: str, password: str):
    '''
        Register User
    '''
    hashed_password = hash_password(password)
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        return {"message": "User registered successfully"}
    except sqlite3.IntegrityError:
        return {"error": "Username already exists"}
    finally:
        conn.close()

