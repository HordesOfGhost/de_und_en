from doctr.io import DocumentFile
from doctr.models import ocr_predictor

model = ocr_predictor(det_arch='db_resnet50', reco_arch='crnn_vgg16_bn', pretrained=True, assume_straight_pages=False,)
# PDF
doc = DocumentFile.from_images("test_german.jpeg")
# Analyze
result = model(doc)
result.show()