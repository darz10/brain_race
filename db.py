from asyncpg import create_pool
import aioredis

from settings import settings

pool = None

async def get_redis_conn():
    return await aioredis.from_url(settings.redis_conn)


class BrainRaceDB:
    """Класс отвечающий за запросы к бд"""
    def __init__(self, psql_conn):
        self.psql_conn = psql_conn

    async def get_asyncpg_pool(self):
        global pool
        if pool is None:
            pool = await create_pool(self.psql_conn, max_size=90)
        return pool


    async def get_user(self, username: str):
        """Получение данных о пользователе"""
        db = await self.get_asyncpg_pool()
        async with db.acquire() as c:
            return await c.fetchrow(
                """
                SELECT username, user_id, first_name, second_name, hashed_password, email, role_id, disabled
                FROM users
                WHERE username = $1
                """,
                username,
            )


    async def add_new_user(
        self,
        username: str,
        first_name: str,
        second_name: str,
        password: str,
        email: str,
    ):
        """Добавление нового пользователя в бд"""
        db = await self.get_asyncpg_pool()
        async with db.acquire() as c:
            await c.execute(
                """
                INSERT INTO users(username, first_name, second_name, hashed_password, email) 
                VALUES ($1, $2, $3, $4, $5)
                """,
                username,
                first_name,
                second_name,
                password,
                email,
            )


    async def update_user(
        self,
        user_id: int,
        first_name: str,
        second_name: str,
        username: str,
        password: str,
        email: str,
    ):
        """Обновление данных о пользователе в бд"""
        db = await self.get_asyncpg_pool()
        async with db.acquire() as c:
            await c.execute(
                """
                UPDATE users(first_name, second_name, username, hashed_password, email)
                SET first_name = $1, second_name = $2, username = $3, hashed_password = $4, email = $5)
                WHERE user_id = $6
                """,
                first_name,
                second_name,
                username,
                password,
                email,
                user_id,
            )


    async def get_user(self, username: str):
        """Получение данных о пользователе"""
        db = await self.get_asyncpg_pool()
        async with db.acquire() as c:
            return await c.fetchrow(
                """
                SELECT username, user_id, first_name, second_name, hashed_password, email, role_id, disabled, user_level, current_car_id
                FROM users
                WHERE username = $1
                """,
                username,
            )


    async def game_user_data(self, username: str):
        """Получение игровых данных о пользователе"""
        db = await self.get_asyncpg_pool()
        async with db.acquire() as c:
            return await c.fetchrow(
                """
                SELECT username, 
                user_id, 
                first_name, 
                second_name, 
                hashed_password, 
                email, 
                role_id, 
                disabled, 
                current_car_id,
                user_level 
                FROM users
                WHERE username = $1
                """,
                username,
            )


    async def get_user_level(self, username: str):
        """Получить уровень игрока"""
        db = await self.get_asyncpg_pool()
        async with db.acquire() as c:
            return await c.execute(
                """
                SELECT user_level
                FROM users 
                WHERE username = $1
                """,
                username,
            )


    async def update_user_level(self, level: int, username: str):
        """Обновить уровень игрока"""
        db = await self.get_asyncpg_pool()
        async with db.acquire() as c:
            return await c.execute(
                """
                UPDATE users 
                SET user_level = $1
                WHERE username = $2
                """,
                level,
                username,
            )


    async def get_user_cars(self, username: str):
        """Получение всех машин пользователя по его username"""
        db = await self.get_asyncpg_pool()
        async with db.acquire() as c:
            return await c.fetch(
                """
                SELECT DISTINCT c.id as car_id, c.car_name, c.description, 
                ARRAY(
                    SELECT DISTINCT color_name 
                    from user_to_car utc
                    INNER JOIN car c ON c.id = utc.car_id
                    INNER JOIN car_to_color ctc ON ctc.color_id = c.id
                    INNER JOIN color ON color.color_id = ctc.color_id
                    where username = $1
                    ) as color_name,
                model_name
                FROM user_to_car utc
                INNER JOIN car c ON c.id = utc.car_id
                INNER JOIN car_to_color ctc ON ctc.color_id = c.id
                INNER JOIN color ON color.color_id = ctc.color_id
                INNER JOIN model m ON c.model_id = m.model_id
                INNER JOIN users u ON u.user_id = utc.user_id
                WHERE u.username = $1
                """,
                username,
            )

    async def upd_curr_car_user(self, user_id: int, car_id: int):
        """Изменение текущей машины пользователя"""
        db = await self.get_asyncpg_pool()
        async with db.acquire() as c:
            return await c.fetch(
                """
                UPDATE user_to_car 
                SET user_id = $1, car_id = $2
                """,
                user_id,
                car_id
            )
