from services.models import doctr_model
import numpy as np
import cv2
import base64
from services.ocr.utils import fix_and_join_overlapping_or_close_boxes, translate_for_ocr, replace_image_with_translated_text
from services.models import gemini_model
from services.ocr.prompt import get_prompt_for_ocr_translation

def scan_and_translate(image_bytes: bytes, direction: str):
    """
    Performs OCR on an image and translates the detected text between English and German.
    The translated text is then rendered back onto the image.

    Parameters
    -----------
    image_bytes : bytes
        The raw byte content of the image to be processed.

    direction : str
        Translation direction. Must be either:
        - "en_to_de" for English to German
        - "de_to_en" for German to English

    Returns
    --------
    tuple[str, str]
        A tuple containing:
        - Base64-encoded original image
        - Base64-encoded image with translated text

    Workflow
    ---------
    1. Decodes the image and applies OCR using Doctr.
    2. Cleans and merges overlapping or nearby text boxes.
    3. Prepares a prompt and translates the extracted text using Gemini.
    4. Replaces the original text in the image with its translation.
    5. Returns both the original and translated images as base64 strings.
    """

    img_array = np.frombuffer(image_bytes, np.uint8)
    original_cv2_img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    ocr_inference = doctr_model([original_cv2_img])
    json_inference_output = ocr_inference.export()
    ocr_data = json_inference_output['pages'][0]['blocks'][0]
    height,width = json_inference_output['pages'][0]['dimensions']

    fixed_ocr_data = fix_and_join_overlapping_or_close_boxes(ocr_data, height, width)
    combined_text = "\n".join([f"{idx+1}. {item['text']}" for idx, item in enumerate(fixed_ocr_data)])

    if direction=="en_to_de":
        prompt_for_ocr_translation = get_prompt_for_ocr_translation(lng1="English", lng2="German",combined_text=combined_text )
        translated_ocr_data = translate_for_ocr(gemini_model, prompt_for_ocr_translation, fixed_ocr_data)
    elif direction=="de_to_en":
        prompt_for_ocr_translation = get_prompt_for_ocr_translation(lng1="German", lng2="English",combined_text=combined_text )
        translated_ocr_data = translate_for_ocr(gemini_model, prompt_for_ocr_translation, fixed_ocr_data)

    translated_cv2_img = replace_image_with_translated_text(original_cv2_img, translated_ocr_data)

    _, original_img_encoded = cv2.imencode('.PNG', original_cv2_img)
    original_base64 = base64.b64encode(original_img_encoded).decode('utf-8')

    _, translated_img_encoded = cv2.imencode('.PNG', translated_cv2_img)
    translated_base64 = base64.b64encode(translated_img_encoded).decode('utf-8')

    return original_base64, translated_base64