from fastapi import FastAPI, UploadFile, File
from detect_utils import analyze_image

app = FastAPI()

@app.post("/batch-analyze/")
async def batch_analyze(files: list[UploadFile] = File(...)):
    results = []

    for file in files:
        image_bytes = await file.read()
        result = analyze_image(image_bytes)
        results.append({
            "filename": file.filename,
            "result": result
        })

    return results

@app.post("/analyze/")
async def analyze(file: UploadFile = File(...)):
    contents = await file.read()
    result = analyze_image(contents)
    return result

@app.get("/hello")
def say_hello():
    return {"message": "안녕하세요!"}