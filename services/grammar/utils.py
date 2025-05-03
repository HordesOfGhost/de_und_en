import re

def extract_raw_html(text: str) -> str:
    """
    Extracts HTML content from a string that may contain code fences (e.g., Markdown-style).

    This function looks for HTML enclosed in ```html ... ``` or generic ``` ... ``` blocks.
    If no such code fences are found, the entire string is assumed to be raw HTML and returned as-is.

    Parameters
    -----------
    text : str
        The input string potentially containing HTML wrapped in code fences.

    Returns
    --------
    str
        The extracted HTML content without code fences or the raw string if no code fences are present.
    """

    match = re.search(r"```html(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    
    match = re.search(r"```(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    
    return text.strip()
