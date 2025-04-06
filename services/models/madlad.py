import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = AutoTokenizer.from_pretrained("google/madlad400-3b-mt")

model = AutoModelForSeq2SeqLM.from_pretrained(
    "google/madlad400-3b-mt",
    device_map="auto",             
    load_in_4bit=True              
)