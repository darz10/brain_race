from fastapi import APIRouter, Depends
from auth.auth import get_current_user
from auth.schemas import User
from race.services import get_user_game_data

router = APIRouter()


@router.get("/")
async def get_main_data(current_user: User = Depends(get_current_user)):
    game_data = await get_user_game_data(current_user["username"])
    result = {
        "username":current_user["username"],
        "first_name": current_user["first_name"],
    }
    if game_data:
        result.update({"car": game_data["car"], "user_level": game_data["user_level"]})
    return result