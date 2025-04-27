from fastapi import UploadFile, Form, File, APIRouter, Request
from fastapi.responses import JSONResponse, HTMLResponse
# from services.ocr import process_image

from routers.config import templates
import random

router = APIRouter()

@router.get("/ocr", response_class=HTMLResponse, include_in_schema=False)
async def upload_or_capture_image(request: Request):
    return templates.TemplateResponse("ocr.html", {"request": request})

@router.post("/ocr")
async def upload_image(
    file: UploadFile = File(...),
    direction: str = Form(...)
):
    # original_base64, translated_base64 = process_image(file, direction)
    original_base64, translated_base64 = "",""


    return JSONResponse(content={
        "original_image": original_base64,
        "translated_image": translated_base64
    })
