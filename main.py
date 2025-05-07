from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from datetime import datetime
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import glob
import json

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/images", StaticFiles(directory="uploads"), name="images")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload")
async def upload_file(
    name: str = Form(...),
    email: str = Form(...),
    description: str = Form(""),
    image: UploadFile = File(...)
):
    filename = f"{datetime.now().timestamp()}_{image.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as f:
        f.write(await image.read())
    info_path = os.path.join(UPLOAD_DIR, f"{filename}_info.txt")
    with open(info_path, "w", encoding="utf-8") as f:
        f.write(f"Họ tên: {name}\nEmail: {email}\nMô tả: {description}\nHình ảnh: {filename}\n")
    return "Thông tin đã được tải lên thành công!"

@app.get("/list")
def list_uploads():
    results = []
    for txt_file in glob.glob("uploads/*_info.txt"):
        with open(txt_file, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
            info = {line.split(": ", 1)[0]: line.split(": ", 1)[1] for line in lines if ": " in line}
            image_file = info.get("Hình ảnh", "")
            info["image_url"] = f"/images/{image_file}"
            results.append(info)
    return results