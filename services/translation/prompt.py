def get_prompt_for_language_translation(lng1, lng2, text):
    prompt = f"""
    Translate the following text. Please only provide the translation and no explanation.

    Source Language: {lng1}
    Target Language: {lng2}
    Text: "{text}"

    Translation:
    """
    return prompt