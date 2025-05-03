import math
import cv2
import textwrap
from services.ocr.config import min_distance_ratio

def boxes_are_close(box1, box2, min_distance_ratio, img_width, img_height):
    """
    Determines whether two bounding boxes are close enough to be considered part of the same text group.
    
    Two boxes are considered close if they touch, overlap, or the distance between them is less than
    a specified fraction of the image diagonal.

    Parameters
    -----------
    box1, box2 : tuple
        Tuples representing two bounding boxes ((x1, y1), (x2, y2)) in absolute pixel values.
    min_distance_ratio : float
        A ratio of the image diagonal used as the threshold distance.
    img_width : int
        Width of the image in pixels.
    img_height : int
        Height of the image in pixels.

    Returns
    --------
    bool
        True if boxes are overlapping, touching, or close enough. False otherwise.
    """

    (x1a, y1a), (x2a, y2a) = box1
    (x1b, y1b), (x2b, y2b) = box2

    # Calculate minimum distance in pixels
    img_diagonal = math.sqrt(img_width**2 + img_height**2)
    min_distance = min_distance_ratio * img_diagonal

    # Check overlap
    if not (x2a < x1b or x2b < x1a or y2a < y1b or y2b < y1a):
        return True  # overlap or touch

    # Compute closest horizontal distance
    if x2a < x1b:
        dx = x1b - x2a
    elif x2b < x1a:
        dx = x1a - x2b
    else:
        dx = 0

    # Compute closest vertical distance
    if y2a < y1b:
        dy = y1b - y2a
    elif y2b < y1a:
        dy = y1a - y2b
    else:
        dy = 0

    # Euclidean distance between closest edges
    distance = math.sqrt(dx**2 + dy**2)
    return distance <= min_distance


def fix_and_join_overlapping_or_close_boxes(ocr_data, height, width):
    """
    Merges overlapping or nearby OCR word boxes into unified text groups.

    Parameters
    -----------
    ocr_data : dict
        Parsed OCR output containing normalized coordinates and text.
    height : int
        Height of the image in pixels.
    width : int
        Width of the image in pixels.

    Returns
    --------
    list[dict]
        A list of merged boxes with absolute pixel coordinates and combined text.
    """

    joined_ocr_data = []

    for line in ocr_data['lines']:
        for word in line['words']:
            word_text = word['value']
            (x1_norm, y1_norm), (x2_norm, y2_norm) = word['geometry']
            x1_abs, y1_abs = int(x1_norm * width), int(y1_norm * height)
            x2_abs, y2_abs = int(x2_norm * width), int(y2_norm * height)
            new_box = ((x1_abs, y1_abs), (x2_abs, y2_abs))

            placed = False
            for group in joined_ocr_data:
                if boxes_are_close(group['box'], new_box, min_distance_ratio, width, height):
                    # Merge with existing group
                    group['text'] += ' ' + word_text
                    (gx1, gy1), (gx2, gy2) = group['box']
                    group['box'] = (
                        (min(gx1, x1_abs), min(gy1, y1_abs)),
                        (max(gx2, x2_abs), max(gy2, y2_abs))
                    )
                    placed = True
                    break

            if not placed:
                joined_ocr_data.append({
                    'text': word_text,
                    'box': new_box
                })
    return joined_ocr_data


def translate_for_ocr(gemini_model, prompt, results):
    """
    Uses the Gemini model to translate grouped OCR text.

    Parameters
    -----------
    gemini_model : object
        A model instance capable of generating content via `.generate_content()`.
    prompt : str
        Formatted prompt containing the OCR text for translation.
    results : list[dict]
        OCR output with each entry containing a 'text' and 'box'.

    Returns
    --------
    list[dict]
        List of translated text with original bounding boxes.
    """

    response = gemini_model.generate_content(prompt)

    translated_lines = response.text.strip().split("\n")
    translated_texts = [line.split(". ", 1)[1] for line in translated_lines]

    translated_json = []
    for idx, item in enumerate(results):
        translated_json.append({
            "text": translated_texts[idx],
            "box": item["box"]
        })

    return translated_json

def replace_image_with_translated_text(original_cv2_img, translated_ocr_data):
    """
    Draws translated text back onto an image by replacing the original OCR regions.

    Parameters
    -----------
    original_cv2_img : np.ndarray
        Original image as a NumPy array (BGR format).
    translated_ocr_data : list[dict]
        List containing translated text and bounding box info.

    Returns
    --------
    np.ndarray
        Image with translated text rendered in place of original text.
    """

    translated_cv2_img = original_cv2_img.copy()

    for res in translated_ocr_data:
        (x1, y1), (x2, y2) = res['box']
        translated_text = res.get('translated_text', res['text'])

        box_width = x2 - x1
        box_height = y2 - y1

        # Step 1: erase old text
        cv2.rectangle(translated_cv2_img, (x1, y1), (x2, y2), (255, 255, 255), thickness=-1)

        # Step 2: find best font_scale
        font = cv2.FONT_HERSHEY_SIMPLEX
        thickness = 1

        # Start from bigger font size, then decrease if necessary
        font_scale = 1.0
        while font_scale > 0:
            (char_width, char_height), _ = cv2.getTextSize("A", font, font_scale, thickness)
            max_chars_per_line = max(1, box_width // char_width)

            wrapped_lines = textwrap.wrap(translated_text, width=max_chars_per_line)
            total_text_height = len(wrapped_lines) * (char_height + 5)

            if total_text_height <= box_height:
                break  # good, fits inside the box
            font_scale -= 0.05  # otherwise try smaller font size

        # Step 3: draw wrapped lines
        current_y = y1 + char_height

        for line in wrapped_lines:
            if current_y > y2:
                break

            cv2.putText(
                translated_cv2_img,
                line,
                (x1, current_y),
                font,
                font_scale,
                (0, 0, 0),
                thickness,
                lineType=cv2.LINE_AA
            )
            current_y += char_height + 5
    return translated_cv2_img