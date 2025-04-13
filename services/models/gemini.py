import google.generativeai as genai  
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)  

gemini_model = genai.GenerativeModel("gemini-2.0-flash")

