from contextlib import asynccontextmanager

from fastapi import FastAPI

from database.models import BaseModel
from database.setup_db import DataBase




@asynccontextmanager
async def lifespain(app: FastAPI):
    async with DataBase.engine.begin() as db:
        await db.run_sync(BaseModel.metadata.create_all)
    yield
