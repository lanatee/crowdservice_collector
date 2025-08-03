import base64
from io import BytesIO
from PIL import Image
import requests


url = "http://localhost:8080/batch-analyze/"
image_paths = [
    "kwanganri/kwanganri_1.jpg",
    "kwanganri/kwanganri_2.jpg",
    "kwanganri/kwanganri_3.jpg",
    "kwanganri/kwanganri_4.jpg",
    "kwanganri/kwanganri_5.jpg"
]  # 분석할 이미지들

files = []
try:
    for path in image_paths:
        files.append(('files', (path, open(path, 'rb'), 'image/jpeg')))
except FileNotFoundError as e:
    print(f"❌ 파일을 찾을 수 없습니다: {e}")
    exit(1)

# 요청 보내기
response = requests.post(url, files=files)

# 응답 디버깅
print("📦 응답 코드:", response.status_code)
try:
    result = response.json()
except Exception as e:
    print("❌ 응답 본문이 JSON이 아닙니다.")
    print("본문 내용:", response.text)
    exit(1)

# 결과 출력 및 이미지 보기
for i, item in enumerate(result):
    print(f"\n[{item['filename']}] 🚶: {item['result']['person_count']} / 🚗: {item['result']['vehicle_count']}")

    try:
        # base64 → 이미지 보기
        img_data = base64.b64decode(item['image_base64'])
        image = Image.open(BytesIO(img_data))
        image.show()
    except Exception as e:
        print(f"❌ 이미지 디코딩 실패: {e}")