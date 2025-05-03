from fastapi import (
    UploadFile, 
    APIRouter, 
    Request,
    Form, 
    File, 
    )
from fastapi.responses import (
    JSONResponse, 
    HTMLResponse,
    )
from services.ocr import scan_and_translate
from routers.config import templates

router = APIRouter()

@router.get("/ocr", response_class=HTMLResponse, include_in_schema=False)
async def render_ocr_page(request: Request):
    """
    Renders the OCR page for image upload or capture.

    Parameters
    -----------
    request : Request
        The incoming HTTP request object for rendering HTML.

    Returns
    --------
    HTMLResponse
        The rendered OCR page with an upload or capture form.
    """
    return templates.TemplateResponse("ocr.html", {
        "request": request
    })

@router.post("/ocr", tags=['ocr'])
async def upload_scan_and_translate(
    file: UploadFile = File(...),
    direction: str = Form("de_to_en")
):
    """
    Handles the image upload, scans it, and returns translated images.

    Parameters
    -----------
    file : UploadFile
        The image file uploaded by the user.
    direction : str
        The translation direction (e.g., "de_to_en" for German to English).

    Returns
    --------
    JSONResponse
        The original and translated image content in JSON format.
    """

    img_bytes = await file.read()

    original_image, translated_image = scan_and_translate(img_bytes, direction)

    return JSONResponse(content={
        "original_image": original_image,
        "translated_image": translated_image
    })
