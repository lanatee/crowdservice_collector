import base64
import io
import uvicorn
from fastapi import FastAPI, UploadFile, File
from detect_utils import analyze_image_return_image

app = FastAPI()

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

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)