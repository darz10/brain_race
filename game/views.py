from typing import List
from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
    Depends,
)
from starlette.responses import HTMLResponse
from game.enum import TypeMessage

# from auth.auth import get_current_user

# from auth.schemas import User
from game.game_services import Timer, game
from game.schemas import Task
from settings import settings


router = APIRouter()


MAX_PLAYER = 2


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        if len(self.active_connections) >= MAX_PLAYER:
            await websocket.accept()
            await websocket.close(
                4000
            )  # TODO кинуть сообщение клиенту что все места заняты
        await websocket.accept()
        self.active_connections.append(websocket)
        await self.broadcast(f"Client # connect the game", TypeMessage.MESSAGE.name)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        data = {"message": message}
        await websocket.send_json(data)

    async def broadcast(self, message: str, type: TypeMessage=None):
        for connection in self.active_connections:
            data = {
                "message": message, 
                "type": type or None
                }
            await connection.send_json(data)

    async def send_question(self, task):
        task_data = Task(
            question=task.get("question"),
            answer1=task.get("answer1"),
            answer2=task.get("answer2"),
            answer3=task.get("answer3"),
            answer4=task.get("answer4"),
        )
        for connection in self.active_connections:
            await connection.send_json(task_data.json())


manager = ConnectionManager()
timer = Timer()


@router.websocket("/ws_game")
async def start_game(websocket: WebSocket):
    token = websocket.headers.get("authorization", None)
    # if not token:
    #     await manager.disconnect()
    # current_user = await get_current_user(token=token)
    await manager.connect(websocket)
    if len(manager.active_connections) == 2:
        await game.get_random_task()
        for task in game.all_question:
            await manager.send_question(task)
            await timer.countdown(task.get("time").seconds, manager)
            user_answer = await websocket.receive_text()
            if user_answer:
                check = await game.check_answer(
                    user_answer, task.get("right_answer")
                )
                if check:
                    await game.record_answer()
                    await timer.break_countdown()
            continue
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Message text was {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client # left the game", TypeMessage.MESSAGE.name)
    finally:
        await manager.disconnect()
