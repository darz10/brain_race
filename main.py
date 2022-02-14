from asyncio import get_event_loop
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from db import BrainRaceDB
from auth import auth, reg_user
from race import views
from game import views as game_views
from settings import settings

app = FastAPI()

db = BrainRaceDB(settings.psql_conn)

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
    app.state.db = await db.get_asyncpg_pool()


app.include_router(auth.router)
app.include_router(reg_user.router)
app.include_router(views.router)
app.include_router(game_views.router)
