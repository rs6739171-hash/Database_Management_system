from redis.asyncio import Redis
from app.config import db_settings

_db = Redis.from_url(url = db_settings.REDIS_URL,decode_responses=True)

async def add_jti_to_blacklist(jti:str):
  await  _db.set(jti,'blacklisted')

async def is_jti_blacklisted(jti: str) -> bool:
    return bool(await _db.exists(jti))