from asyncpg import create_pool
from settings import settings

pool = None


async def get_asyncpg_pool():
    global pool
    if pool is None:
        pool = await create_pool(settings.psql_conn, max_size=90)
    return pool
