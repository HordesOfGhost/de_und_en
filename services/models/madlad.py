from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, BitsAndBytesConfig
from .config import device


quantization_config = BitsAndBytesConfig(load_in_8bit=True)

madlad_tokenizer = AutoTokenizer.from_pretrained("google/madlad400-3b-mt")

madlad_model = AutoModelForSeq2SeqLM.from_pretrained(
    "google/madlad400-3b-mt",
    device_map="auto",         
    quantization_config=quantization_config              
)