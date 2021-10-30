from fastapi import APIRouter, Depends
from auth.auth import get_current_user
from auth.schemas import User
from race.services import get_user_game_data

router = APIRouter()


@router.get("/")
async def get_main_data(current_user: User = Depends(get_current_user)):
    game_data = await get_user_game_data(current_user["username"])
    return game_data