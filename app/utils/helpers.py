from redis import asyncio as aioredis

from app.config import settings


class RedisHelper:
    def __init__(self):
        self.redis_client: aioredis.Redis | None = None

    async def connect(self):
        if self.redis_client is None:
            self.redis_client = await aioredis.from_url(
                f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
                encoding="utf8",
                decode_responses=True,
            )

    async def close(self):
        if self.redis_client:
            await self.redis_client.close()
            self.redis_client = None

    async def log_to_redis(self, message: dict):
        if self.redis_client is None:
            await self.connect()
        await self.redis_client.rpush("logs", str(message))


redis_helper = RedisHelper()
