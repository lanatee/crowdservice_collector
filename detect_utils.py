import psycopg2
import torch
from PIL import Image
from datetime import datetime
import os
from io import BytesIO

model = torch.hub.load('yolov5', 'yolov5x', source='local')  # yolov5x.pt 불러오기
model.eval()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "crowdinfodb")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "admin123")

def save_analysis_to_db(person_count: int, vehicle_count: int):
    analyzed_at = datetime.now()
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO crowdanalysis (analyzed_at, person_count, vehicle_count)
            VALUES (%s, %s, %s)
        """, (analyzed_at, person_count, vehicle_count))
        conn.commit()
        cur.close()
        conn.close()
        print(f"✅ DB 저장 완료: {analyzed_at} 기준")
    except Exception as e:
        print("❌ DB 저장 실패:", e)

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

    print("🚶 사람 수:", person_count)
    print("🚗 차량 수:", vehicle_count)

    save_analysis_to_db(person_count, vehicle_count)

    return {
        "person_count": person_count,
        "vehicle_count": vehicle_count
    }
