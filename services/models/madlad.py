from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from .config import device

madlad_tokenizer = AutoTokenizer.from_pretrained("google/madlad400-3b-mt")

madlad_model = AutoModelForSeq2SeqLM.from_pretrained(
    "google/madlad400-3b-mt",
    device_map="auto",             
    load_in_4bit=True              
)