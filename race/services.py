from db import get_redis_conn


async def get_user_game_data(current_user):
    """Получение игровых данных пользователя"""
    try:
        redis = await get_redis_conn()
        username = current_user["username"]
        curr_exp = await redis.get(f"br:{username}:curr_exp")
        game_user_data = {
            "username": current_user.get("username"),
            "user_id": current_user["user_id"],
            "first_name": current_user["first_name"],
            "role_id": current_user["role_id"],
            "disabled": current_user["disabled"],
            "user_level": current_user["user_level"],
            "current_car_id": current_user["current_car_id"],
        }
        if curr_exp:
            game_user_data.update({"curr_exp": int(curr_exp.decode())})
        return game_user_data
    except Exception as e:
        print(e)


class UserLevel:
    """Класс ответственный за действия связанные с уровнем игрока"""

    def __init__(self, username: str, BrainRaceDB):
        self.username = username
        self.db = BrainRaceDB

    async def update_level(self, level: int, username: str):
        """Увеличение значения уровня"""
        try:
            await self.db.update_user_level(level, username)
        except Exception as e:
            print(e)

    async def get_user_level(self, username: str):
        """Получение уровня игрока"""
        try:
            level = await self.db.get_user_level(username)
            return level
        except Exception as e:
            print(e)


class Car:
    """Класс описывающий характеристики и действия машин"""

    def __init__(self, BrainRaceDB):
        self.db = BrainRaceDB

    async def get_avalible_user_cars(self, username: str):
        """Получение всех машин пренадлежащих пользователю"""
        try:
            user_cars = await self.db.get_user_cars(username)
            if user_cars:
                return user_cars
        except Exception as e:
            print(e)

    async def update_curr_car_user(self, user_id: int, car_id: int):
        """Изменение текущей машины пользователя"""
        try:
            await self.db.upd_curr_car_user(user_id, car_id)
        except Exception as e:
            print(e)
