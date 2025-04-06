from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from services.translation import convert_to_de, convert_to_en


app = FastAPI()
templates = Jinja2Templates(directory="templates")

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def landing(request: Request):
    return templates.TemplateResponse("landing.html", {"request": request})

@app.get("/translate", response_class=HTMLResponse)
async def translation_form(request: Request, direction: str):
    return templates.TemplateResponse("translation.html", {
        "request": request,
        "direction": direction,
        "translated_text": ""
    })

@app.post("/translate", response_class=HTMLResponse)
async def translate(request: Request, input_text: str = Form(...), direction: str = Form(...)):
    if direction == "en_to_de":
        input_language = "English"
        translated_language = "German"
        translated_text = convert_to_de(input_text)
    else:
        input_language = "German"
        translated_language = "English"
        translated_text = convert_to_en(input_text)
    
    return templates.TemplateResponse("translation.html", {
        "request": request,
        "input_language":input_language,
        "input_text":input_text,
        "translated_text": translated_text,
        "translated_lanugage": translated_language,
        "direction": direction
    })