from asyncio import get_event_loop
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from db import get_asyncpg_pool
from auth import auth, reg_user
from race import views
from settings import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    app.state.settings = settings
    app.state.loop = get_event_loop()
    app.state.db = await get_asyncpg_pool()


app.include_router(auth.router)
app.include_router(reg_user.router)
app.include_router(views.router)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
