import requests

file_path = "kwanganri_1.jpg"
url = "http://localhost:8080/analyze/"

with open(file_path, "rb") as f:
    files = {'file': f}
    response = requests.post(url, files=files)

print(response.json())