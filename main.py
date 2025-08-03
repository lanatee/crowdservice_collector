import base64
import io
import uvicorn
from fastapi import FastAPI, UploadFile, File
from detect_utils import analyze_image_return_image
from tourlist_collector import *
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 또는 프론트 주소만 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/batch-analyze/")
async def batch_analyze(files: list[UploadFile] = File(...)):
    results = []

    for file in files:
        image_bytes = await file.read()
        try:
            result, result_image = analyze_image_return_image(image_bytes)
        except Exception as e:
            print(f"❌ 분석 실패: {e}")
            raise

        try:
            buffered = io.BytesIO()
            result_image.save(buffered, format="JPEG")
            encoded_image = base64.b64encode(buffered.getvalue()).decode()
        except Exception as e:
            print(f"❌ 이미지 인코딩 실패: {e}")
            raise

        results.append({
            "filename": file.filename,
            "result": result,
            "image_base64": encoded_image
        })

    return results

@app.get("/hello")
def say_hello():
    return {"message": "안녕하세요!"}

@app.post("/collect-tourist-spots")
def collect_spots():
    total = collect_tourist_data_from_api()
    return {"status": "done", "inserted": total}


@app.get("/tourist-spots")
def get_spots():
    spots = get_tourist_spots()
    return spots