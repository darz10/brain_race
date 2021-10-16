from typing import Dict
import db


async def get_user_game_data(username: str) -> Dict:
    redis = await db.connect_redis()
    game_user_data = await redis.get(f"br:game_data:{username}")
    return game_user_data
