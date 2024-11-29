from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import uvicorn

from data_manager import DataManager
from qrcode_admin import QRCodeTool

datamanager = DataManager("../data/qr_codes.db")
qr_tool = QRCodeTool()

# QR code automation
DEFAUTL_LINK = "http://0.0.0.0:9000/qr_code/{data}"

def create_link(data):
    return DEFAUTL_LINK.format(data)


def generate_qr_code():
    with open("file", "r") as file:
        data = file.readlines()

    for i in data:
        link = create_link(i)
        qr_tool.generate_qr(link)
        # data = link.split("/")[-1]
        datamanager.insert_code(data)
    return


# API section

app = FastAPI()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*']
)


@app.get("/qr_code/{data}")
async def validate_qr_code(data: str):
    code = datamanager.get_single_code(data)
    if code[2] == 0:
        datamanager.cursor.execute('''UPDATE codes SET used = 1 WHERE data = ?''', (data,))
        datamanager.conn.commit()
        return {"status": "valid"}
    else:
        return {"status": "invalid"}
    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
