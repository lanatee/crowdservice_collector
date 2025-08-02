from fastapi import FastAPI, UploadFile, File
from detect_utils import analyze_image

app = FastAPI()


@app.post("/analyze/")
async def analyze(file: UploadFile = File(...)):
    contents = await file.read()
    result = analyze_image(contents)
    return result

@app.get("/hello")
def say_hello():
    return {"message": "안녕하세요!"}