from fastapi import APIRouter, Depends
from auth.auth import get_current_user
from auth.schemas import User
from race.schemas import ResponseStatus
from race.services import choice_avalible_user_cars, get_user_game_data

router = APIRouter()


@router.get("/")
async def get_main_data(current_user: User = Depends(get_current_user)):
    game_data = await get_user_game_data(current_user)
    return game_data


@router.get("/choice-car")
async def get_available_cars(current_user: User = Depends(get_current_user)):
    try:
        user_cars = await choice_avalible_user_cars(current_user["username"])
        return
    except Exception as e:
        print(f"{e}")
        return ResponseStatus(
            success=False,
            status_code=400,
            resposne="Error receiving information"
        )