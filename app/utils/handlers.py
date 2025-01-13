import asyncio
import logging

from app.utils.helpers import RedisHelper
from app.utils.helpers import redis_helper
from logging import LogRecord
from typing import Type


class RedisHandler(logging.Handler):
    def __init__(self, redis_helper: Type[RedisHelper]):
        super().__init__()
        self.redis_helper = redis_helper

    async def emit_async(self, record: LogRecord):
        log_entry = self.format(record)
        if self.redis_helper.redis_client is None:
            await self.redis_helper.connect()
        await self.redis_helper.log_to_redis(log_entry)

    def emit(self, record: LogRecord):
        loop = asyncio.get_event_loop()
        loop.create_task(self.emit_async(record))


fileHandler = logging.FileHandler("./logs/logs.json")
redis_handler = RedisHandler(redis_helper)
