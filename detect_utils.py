import torch
from PIL import Image
import numpy as np
from io import BytesIO

#model = torch.hub.load('yolov5', 'yolov5x', source='local')  # yolov5x.pt 불러오기
model = torch.hub.load('ultralytics/yolov5', 'yolov5x', pretrained=True)
model.eval()


def analyze_image(image_bytes: bytes) -> dict:
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    results = model(image, size=640)
    detections = results.pred[0]  # tensor: [x1, y1, x2, y2, conf, class]

    vehicle_ids = [2, 5, 7]
    person_id = 0
    vehicle_count = 0
    person_count = 0

    for *xyxy, conf, cls in detections:
        cls_id = int(cls)
        if cls_id == person_id:
            person_count += 1
        elif cls_id in vehicle_ids:
            vehicle_count += 1

    return {
        "person_count": person_count,
        "vehicle_count": vehicle_count
    }
