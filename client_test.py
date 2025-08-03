import requests

##file_path = "kwanganri_1.jpg"
#url = "http://localhost:8000/analyze/"

#with open(file_path, "rb") as f:
#    files = {'file': f}
#    response = requests.post(url, files=files)

#print(response.json())

url = "http://localhost:8000/batch-analyze/"
image_paths = [
    "kwanganri/kwanganri_1.jpg",
    "kwanganri/kwanganri_2.jpg",
    "kwanganri/kwanganri_3.jpg",
    "kwanganri/kwanganri_4.jpg",
    ]  # 분석할 이미지들

files = []
for path in image_paths:
    files.append(('files', (path, open(path, 'rb'), 'image/jpeg')))

response = requests.post(url, files=files)

print("응답 결과:")
print(response.json())