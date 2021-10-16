from asyncpg import create_pool
from settings import settings

pool = None


async def get_asyncpg_pool():
    global pool
    if pool is None:
        pool = await create_pool(settings.psql_conn, max_size=90)
    return pool


async def get_user(username: str):
    """Получение данных о пользователе"""
    db = await get_asyncpg_pool()
    async with db.acquire() as c:
        return await c.fetchrow(
            """
            SELECT user_id, first_name, second_name, hashed_password, email, role_id, disabled
            FROM users
            WHERE username = $1
            """,
            username,
        )


async def add_new_user(
    first_name: str,
    second_name: str,
    username: str,
    password: str,
    email: str,
    role_id: int,
    disabled: bool,
):
    """Добавление нового пользователя в бд"""
    db = await get_asyncpg_pool()
    async with db.acquire() as c:
        await c.execute(
            """
            INSERT INTO users(username, first_name, second_name, hashed_password, email, role_id, disabled) 
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            """,
            username,
            first_name,
            second_name,
            password,
            email,
            role_id,
            disabled,
        )


async def update_user(
    user_id: int,
    first_name: str,
    second_name: str,
    username: str,
    password: str,
    email: str,
):
    """Обновление данных о пользователе в бд"""
    db = await get_asyncpg_pool()
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
