import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import time

start_time = time.time()


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = AutoTokenizer.from_pretrained("google/madlad400-3b-mt")

model = AutoModelForSeq2SeqLM.from_pretrained(
    "google/madlad400-3b-mt",
    device_map="auto",             # Automatically maps to GPU
    load_in_4bit=True              # Save memory with quantization
)

# Tokenize and move tensors to GPU
inputs = tokenizer("<2de> You want to do it yourself and say you need me.", return_tensors="pt")
inputs = {k: v.to(device) for k, v in inputs.items()}

# Generate output
outputs = model.generate(**inputs)

# Decode
decoded = tokenizer.batch_decode(outputs, skip_special_tokens=True)
print(decoded)
final_time = time.time()


print(final_time - start_time)

