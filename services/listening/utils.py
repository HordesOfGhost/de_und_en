import re
import json

def extract_json_content_from_llm_response(llm_response):
    cleaned_json = re.sub(r"```json|```", "", llm_response).strip()
    cleaned_json = json.loads(cleaned_json)
    return cleaned_json
