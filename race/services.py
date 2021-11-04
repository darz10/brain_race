import db


async def get_user_game_data(current_user):
    """Получение игровых данных пользователя"""
    try:
        redis = await db.get_redis_conn()
        username = current_user["username"]
        curr_exp = await redis.get(f"br:{username}:curr_exp")
        game_user_data = current_user
        if curr_exp:
            game_user_data.update({"curr_exp":curr_exp})
        return game_user_data
    except Exception as e:
        print(e)

async def choice_avalible_user_cars(username: str):
    """Получение всех машин пренадлежащих пользователю"""
    try:
        user_cars = await db.get_user_cars(username)
        if user_cars:
            return user_cars
    except Exception as e:
        print(e)


async def update_level(level, username):
    """Увеличение значения уровня"""
    try:
        await db.update_user_level(level, username)
    except Exception as e:
        print(e)