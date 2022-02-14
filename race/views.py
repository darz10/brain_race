from fastapi import APIRouter, Depends
from pydantic.utils import truncate
from auth.auth import get_current_user
from auth.schemas import User
from db import BrainRaceDB
from race.schemas import ResponseStatus, UpdCar
from race.services import Car, get_user_game_data
from settings import settings

router = APIRouter()


@router.get("/v1/")
async def get_main_data(current_user: User = Depends(get_current_user)):
    try:
        game_data = await get_user_game_data(current_user)
        return game_data
    except Exception as e:
        print(e)  # //TODO logger
        return ResponseStatus(
            success=False,
            status_code=400,
            resposne="Error receiving information",
        )


@router.get("/v1/choice-car")
# //TODO сделать из этого метода 2 эндпоинта для получения всех машин пользователя и для изменения текущей машины
async def get_available_cars(current_user: User = Depends(get_current_user)):
    db = BrainRaceDB(settings.psql_conn)
    car = Car(BrainRaceDB=db)
    try:
        user_cars = await car.get_avalible_user_cars(
            username=current_user["username"]
        )
        return user_cars
    except Exception as e:
        print(e)
        return ResponseStatus(
            success=False,
            status_code=400,
            resposne="Error receiving information",
        )


@router.put("/v1/update-current-car")
async def update_curr_car(
    request_body: UpdCar, current_user: User = Depends(get_current_user)
):
    """Изменение выбора текущей машины"""
    db = BrainRaceDB(settings.psql_conn)
    car = Car(BrainRaceDB=db)
    try:
        user_cars = await car.get_avalible_user_cars(
            username=current_user["username"]
        )
        return ResponseStatus(
            success=truncate,
            status_code=200,
            resposne="Current car updated successfully",
        )
    except Exception as e:
        print(e)
        return ResponseStatus(
            success=False,
            status_code=400,
            resposne="Сurrent сar has not been updated.",
        )