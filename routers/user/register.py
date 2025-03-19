from fastapi import APIRouter, HTTPException, Form
from services.user import register_user

router = APIRouter()

@router.post("/register/")
async def user_register(username: str = Form(...), password: str = Form(...)):
    '''
        Register user with username and password.
    '''
    result = register_user(username, password)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result