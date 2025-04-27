from doctr.io import DocumentFile
from doctr.models import ocr_predictor

doctr_model = ocr_predictor(det_arch='db_resnet50', reco_arch='crnn_vgg16_bn', pretrained=True,assume_straight_pages=False,detect_language=True, export_as_straight_boxes=True)