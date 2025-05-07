from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from datetime import datetime

app = FastAPI()

# Cho phép CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho frontend gọi API
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload")
async def upload_file(
    name: str = Form(...),
    email: str = Form(...),
    description: str = Form(""),
    image: UploadFile = File(...)
):
    # Lưu hình ảnh
    filename = f"{datetime.now().timestamp()}_{image.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as f:
        f.write(await image.read())

    # Lưu thông tin text
    info_path = os.path.join(UPLOAD_DIR, f"{filename}_info.txt")
    with open(info_path, "w", encoding="utf-8") as f:
        f.write(f"Họ tên: {name}\nEmail: {email}\nMô tả: {description}\nHình ảnh: {filename}\n")

    return JSONResponse(content={"message": "Thông tin đã được gửi thành công!"})
