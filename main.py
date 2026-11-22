from app.api import routers
from app.database.session import create_db_table
from fastapi.concurrency import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_table()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(routers.router)
