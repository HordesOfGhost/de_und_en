import re
import json

def extract_json_content_from_llm_response(llm_response):
    """
    Extracts and parses JSON content from a language model's response.

    Assumes the JSON is enclosed within Markdown-style code fences (e.g., ```json ... ```).
    Strips the code fences and parses the remaining string into a Python dictionary.

    Parameters:
    -----------
    llm_response : str
        The raw response from the language model, expected to contain a JSON block.

    Returns:
    --------
    dict
        Parsed JSON content as a Python dictionary.

    Raises:
    -------
    json.JSONDecodeError
        If the cleaned string is not valid JSON.
    """
    cleaned_json = re.sub(r"```json|```", "", llm_response).strip()
    cleaned_json = json.loads(cleaned_json)
    return cleaned_json
