from services.models import doctr_model
import numpy as np
import cv2
import base64
from services.ocr.utils import fix_and_join_overlapping_or_close_boxes, translate_for_ocr, replace_image_with_translated_text
from services.models import gemini_model
from services.ocr.prompt import prompt

def scan_and_translate(image_bytes, direction):
    img_array = np.frombuffer(image_bytes, np.uint8)
    original_cv2_img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    ocr_inference = doctr_model([original_cv2_img])
    json_inference_output = ocr_inference.export()
    ocr_data = json_inference_output['pages'][0]['blocks'][0]
    height,width = json_inference_output['pages'][0]['dimensions']

    fixed_ocr_data = fix_and_join_overlapping_or_close_boxes(ocr_data, height, width)
    combined_text = "\n".join([f"{idx+1}. {item['text']}" for idx, item in enumerate(fixed_ocr_data)])

    if direction=="en_to_de":
        prompt_for_ocr_translation = prompt.format(lng1="English", lng2="German",combined_text=combined_text )
        translated_ocr_data = translate_for_ocr(gemini_model, prompt_for_ocr_translation, fixed_ocr_data)
    elif direction=="de_to_en":
        prompt_for_ocr_translation = prompt.format(lng1="German", lng2="English",combined_text=combined_text )
        translated_ocr_data = translate_for_ocr(gemini_model, prompt_for_ocr_translation, fixed_ocr_data)

    translated_cv2_img = replace_image_with_translated_text(original_cv2_img, translated_ocr_data)

    _, original_img_encoded = cv2.imencode('.PNG', original_cv2_img)
    original_base64 = base64.b64encode(original_img_encoded).decode('utf-8')

    _, translated_img_encoded = cv2.imencode('.PNG', translated_cv2_img)
    translated_base64 = base64.b64encode(translated_img_encoded).decode('utf-8')

    return original_base64, translated_base64