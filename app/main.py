import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from app.database import Base, engine
from app.item.router import router as item_router
from app.logger import logger
from app.utils.helpers import redis_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await redis_helper.connect()
        pong = await redis_helper.redis_client.ping()

        logger.info(f"Redis connection status: {pong}")
        FastAPICache.init(RedisBackend(redis_helper.redis_client), prefix="cache")

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        yield
    except Exception as e:
        logger.error(f"Error lifespan setup", exc_info=True)
        raise e
    finally:
        await redis_helper.close()


app = FastAPI(lifespan=lifespan, title="ToDoList", root_path="/api", version="0.1.0")


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    response = {
        "statusCode": exc.status_code,
        "message": exc.detail,
    }
    return JSONResponse(status_code=exc.status_code, content=response)


app.include_router(item_router)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    log_data = {
        "process_time": round(process_time, 4),
        "url": request.url,
        "method": request.method,
        "headers": dict(request.headers),
    }
    logger.info("Request information", extra=log_data)
    return response
