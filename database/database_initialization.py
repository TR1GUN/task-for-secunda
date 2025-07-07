from database.models import _BaseModel
from database.setup_db import DataBase
from contextlib import asynccontextmanager
from fastapi import FastAPI


@asynccontextmanager
async def lifespain(app: FastAPI):
    async with DataBase.engine.begin() as db:
        await db.run_sync(_BaseModel.metadata.create_all)
    yield
