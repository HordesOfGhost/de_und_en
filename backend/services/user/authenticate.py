from services.database import get_db_connection
from .auth import verify_password

def authenticate_user(username: str, password: str):
    '''
        Authenticate User
    '''
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if user and verify_password(password, user["password"]):
        return {"message": "Login successful"}
    return {"error": "Invalid username or password"}
