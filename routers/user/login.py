from fastapi import APIRouter, HTTPException, Form
from services.user import authenticate_user

router = APIRouter()

@router.post("/login/")
async def user_login(username: str = Form(...), password: str = Form(...)):
    '''
        Login user with username and password.
    '''
    result = authenticate_user(username, password)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result
