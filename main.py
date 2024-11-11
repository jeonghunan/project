from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import qrcode
from io import BytesIO
from pydantic import BaseModel
from typing import List

app = FastAPI()

# 데이터를 저장할 리스트
board_data = []


# BoardData 모델
class BoardData(BaseModel):
    number: int
    boardName: str
    repairHistory: str

# Static files (CSS, JS, images) 경로 설정
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates 경로 설정
templates = Jinja2Templates(directory="templates")

# 기본 HTML 페이지
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/boardfix", response_class=HTMLResponse)
async def read_boardfix(request: Request):
    return templates.TemplateResponse("boardfix.html", {"request": request})

@app.get("/material", response_class=HTMLResponse)
async def read_material(request: Request):
    return templates.TemplateResponse("material.html", {"request": request})

@app.get("/mbt_button", response_class=HTMLResponse)
async def read_boardfix(request: Request):
    return templates.TemplateResponse("mbt_button.html", {"request": request})

@app.get("/ssd_button", response_class=HTMLResponse)
async def read_boardfix(request: Request):
    return templates.TemplateResponse("ssd_button.html", {"request": request})

@app.get("/soc_button", response_class=HTMLResponse)
async def read_boardfix(request: Request):
    return templates.TemplateResponse("soc_button.html", {"request": request})

@app.get("/ssd_button_ft", response_class=HTMLResponse)
async def read_boardfix(request: Request):
    return templates.TemplateResponse("ssd_button_ft.html", {"request": request})

@app.get("/ssd_button_tg", response_class=HTMLResponse)
async def read_boardfix(request: Request):
    return templates.TemplateResponse("ssd_button_tg.html", {"request": request})

@app.get("/ssd_button_pg", response_class=HTMLResponse)
async def read_boardfix(request: Request):
    return templates.TemplateResponse("ssd_button_pg.html", {"request": request})

@app.get("/mbt_button_ft", response_class=HTMLResponse)
async def read_boardfix(request: Request):
    return templates.TemplateResponse("mbt_button_ft.html", {"request": request})

class BoardData(BaseModel):
    number: int
    boardName: str
    repairHistory: str

# 클라이언트로부터 받은 데이터 저장
@app.post("/save_board_data")
async def save_board_data(board_data_list: List[BoardData]):
    global board_data
    board_data = board_data_list  # 클라이언트에서 보낸 데이터로 리스트를 갱신
    return {"message": "데이터 저장 완료"}

# 클라이언트로부터 데이터를 요청할 때
@app.get("/get_board_data")
async def get_board_data():
    return board_data  # 저장된 데이터를 클라이언트에 반환

# QR 코드 생성 및 반환
@app.get("/qr")
async def generate_qr():
    # QR 코드에 포함될 URL
    url = "http://192.168.57.133:8000/"


    # QR 코드 생성
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # 이미지를 메모리에 저장
    img = qr.make_image(fill="black", back_color="white")
    img_io = BytesIO()
    img.save(img_io, "PNG")
    img_io.seek(0)

    # 이미지 스트림을 통해 QR 코드 반환
    return StreamingResponse(img_io, media_type="image/png")
