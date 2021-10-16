
from fastapi import APIRouter, WebSocket
from main import app

router = APIRouter()


@router.get("/")
async def get_main_data():
    pass


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")