from typing import Dict
import db


async def get_user_game_data(username: str):
    
    return


async def choice_avalible_user_cars(user_id: int):
    user_cars = await db.get_user_cars(user_id)
    return user_cars