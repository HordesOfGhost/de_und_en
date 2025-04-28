from fastapi import UploadFile, Form, File, APIRouter, Request
from fastapi.responses import JSONResponse, HTMLResponse
from services.ocr import scan_and_translate

from routers.config import templates
import random

router = APIRouter()

@router.get("/ocr", response_class=HTMLResponse, include_in_schema=False)
async def upload_or_capture_image(request: Request):
    return templates.TemplateResponse("ocr.html", {"request": request})

@router.post("/ocr", tags=['ocr'])
async def upload_image(
    file: UploadFile = File(...),
    direction: str = Form("de_to_en")
):
    img_bytes = await file.read()
    original_image, translated_image = scan_and_translate(img_bytes, direction)
    return JSONResponse(content={
        "original_image": original_image,
        "translated_image": translated_image
    })
