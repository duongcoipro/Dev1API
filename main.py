from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from datetime import datetime
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import glob
import json
from zlapi import ZaloAPI
from zlapi.models import *

imei = "a7da7a49-9f7e-4fb7-8173-154af9d2af66-f1f6b29a6cc1f79a0fea05b885aa33d0"
cookies = {"_ga_NCLZ4KG7XE":"GS1.1.1729050963.1.1.1729051022.0.0.0","_gcl_au":"1.1.1760086498.1741684853","_ga_NVN38N77J3":"GS1.2.1741685714.2.0.1741685714.0.0.0","_ga_E63JS7SPBL":"GS1.1.1741685713.2.0.1741685718.55.0.0","_ga_1J0YGQPT22":"GS1.1.1741686996.2.1.1741687341.55.0.0","zoaw_sek":"xmje.891775287.2.wvkWGa5M71nsFpifGLOS745M71n1LXmSGB9x42bM71m","zoaw_type":"0","__zi":"3000.SSZzejyD7iu_cVEzsr0LpYAPvhoKKa7GR9V-_yX0IvuWa_ssXqL9coQQiBQ5J0sP9PEzlO913PC.1","__zi-legacy":"3000.SSZzejyD7iu_cVEzsr0LpYAPvhoKKa7GR9V-_yX0IvuWa_ssXqL9coQQiBQ5J0sP9PEzlO913PC.1","_ga":"GA1.2.627150477.1720074500","_gid":"GA1.2.1191676216.1746593671","_zlang":"vn","googtrans":"/auto/vi","_ga_907M127EPP":"GS2.1.s1746597880$o3$g0$t1746597880$j60$l0$h0","_ga_RYD7END4JE":"GS2.2.s1746598038$o6$g1$t1746598080$j18$l0$h0","zpsid":"CRyt.434311158.3.XTy1h9vPmnDeLY0Aabd34-igiIUjRV0YhsZsApMu5FYKgLYSdrKv2VPPmnC","zpw_sek":"EvWr.434311158.a0.d7wkTHTaIZBXQwahDcHACcn6BrarNcXpK14715jN7M8bFGnKNomoPM4FALL6MNSGQi-hvVnkkgcOPKR83GnACW","app.event.zalo.me":"5352338974368243918"}
bot = ZaloAPI("0876089909", "Diamond99!!", imei=imei, cookies=cookies)
msg = Message(text="The system starts automatically at: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#bot.sendMessage(msg, 8046989271300889247, ThreadType.GROUP)


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