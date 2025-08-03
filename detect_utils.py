from PIL import Image
from PIL import ImageDraw
from io import BytesIO
from ultralytics import YOLO

#model = torch.hub.load('yolov5', 'yolov5x', source='local')  # yolov5x.pt 불러오기
#model = torch.hub.load('ultralytics/yolov5', 'yolov5x6', pretrained=True)
model = YOLO("yolov8n.pt")
#model.eval()


def analyze_image_return_image(image_bytes: bytes):
    # image = Image.open(BytesIO(image_bytes)).convert("RGB")
    # results = model(image, size=3000)
    # detections = results.pred[0]
    #
    # draw = ImageDraw.Draw(image)
    #
    # vehicle_ids = [2, 5, 7]
    # person_id = 0
    # vehicle_count = 0
    # person_count = 0
    #
    # for *xyxy, conf, cls in detections:
    #     cls_id = int(cls)
    #     x1, y1, x2, y2 = map(int, xyxy)
    #     if cls_id == person_id:
    #         person_count += 1
    #         draw.rectangle([x1, y1, x2, y2], outline="red", width=2)
    #     elif cls_id in vehicle_ids:
    #         vehicle_count += 1
    #         draw.rectangle([x1, y1, x2, y2], outline="blue", width=2)
    #
    # return {
    #     "person_count": person_count,
    #     "vehicle_count": vehicle_count
    # }, image
    # 1. 이미지 디코딩
    image = Image.open(BytesIO(image_bytes)).convert("RGB")

    # 2. 탐지 실행 (YOLOv8은 size가 아닌 imgsz 사용)
    results = model(image, imgsz=2048, conf=0.1)

    # 3. 결과에서 박스 추출
    detections = results[0].boxes
    draw = ImageDraw.Draw(image)

    # 4. 클래스 정보
    vehicle_names = ['car', 'bus', 'truck', 'motorbike']  # 필요한 경우 bicycle 추가
    person_count = 0
    vehicle_count = 0

    for box in detections:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        class_name = model.names[cls_id]

        if class_name == "person":
            person_count += 1
            draw.rectangle([x1, y1, x2, y2], outline="red", width=2)
        elif class_name in vehicle_names:
            vehicle_count += 1
            draw.rectangle([x1, y1, x2, y2], outline="blue", width=2)

    return {
        "person_count": person_count,
        "vehicle_count": vehicle_count
    }, image

