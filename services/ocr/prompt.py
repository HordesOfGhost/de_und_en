def get_prompt_for_ocr_translation(lng1, lng2, combined_text):
    prompt = f"""
    Translate the following {lng1} sentences into {lng2}. Keep the order, and only return the translated sentences, nothing else:

    {combined_text}
    """
    return prompt
