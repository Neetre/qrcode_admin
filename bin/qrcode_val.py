import os
from fastapi import FastAPI, Form, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.cors import CORSMiddleware
import uvicorn
import argparse
from dotenv import load_dotenv
load_dotenv()
PASSWORD = os.getenv("PASSWORD_ADMIN")

from data_manager import DataManager
from qrcode_admin import QRCodeTool
from send_email import email_sender

datamanager = DataManager("../data/qr_codes.db")
qr_tool = QRCodeTool()


# QR code automation
def create_link(code):
    return DEFAUTL_LINK + code


def generate_qr_code():
    data = datamanager.get_codes()
    c = 1
    for i in data:
        filename = f"qr_code_{c}.png"
        link = create_link(i[1])
        qr_tool.generate_qr(link, filename)
        c += 1
    return


# API section
app = FastAPI()
'''
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*']
)
'''


@app.get("/qr_code", response_class=JSONResponse)
async def validate_qr_code(request: Request):
    code = request.query_params.get("code") or request.query_params.get("data")
    qr_code = datamanager.get_single_code(code)
    if qr_code is None:
        return {"status": "invalid"}

    if qr_code[2] == 0:
        datamanager.cursor.execute('''UPDATE codes SET used = 1 WHERE data = ?''', (code,))
        datamanager.conn.commit()
        return {"status": "valid"}
    else:
        return {"status": "invalid"}


@app.get("/admin_login")
async def admin_login(data: str):
    if data == PASSWORD:
        return {"status": "ok"}
    else:
        return {"status": "invalid"}


@app.get("/generate_qr_codes")
async def generate_qr_codes(password: str):
    if password != PASSWORD:
        return {"status": "invalid password"}
    generate_qr_code()
    return {"status": "ok"}


@app.get("/send_email")
async def send_email(password: str):
    if password != PASSWORD:
        return {"status": "invalid password"}
    email_sender()
    return {"status": "ok"}


def parse_args():
    parser = argparse.ArgumentParser(description='Gestore di codici QR')
    parser.add_argument('-ip', '--ip_address', type=str, help='Indirizzo IP del server')
    parser.add_argument('-d', '--domain', type=str, default="0.0.0.0", help='Dominio del server')
    parser.add_argument('-p', '--port', type=int, default="8000", help='Porta del server')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    DEFAUTL_LINK = f"http://{args.ip_address if not args.domain else args.domain}:{args.port}/qr_code?code="
    uvicorn.run(app, host=args.ip_address if not args.domain else args.domain, port=args.port)
