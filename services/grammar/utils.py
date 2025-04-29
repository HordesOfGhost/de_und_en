import re

def extract_raw_html(text: str) -> str:

    # Match a ```html ... ``` block
    match = re.search(r"```html(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    
    # If triple backticks without html
    match = re.search(r"```(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    
    # If no code fences, assume it's raw HTML already
    return text.strip()
