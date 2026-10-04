from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import OperationalError
from contextlib import asynccontextmanager
import asyncio
from sqlalchemy import text
from settings import database









@asynccontextmanager
async def lifespan(app: FastAPI):
    while True:
        try:
            # Check if the database is ready
            with database.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            break

        except OperationalError:
            print("Database is not ready yet, waiting...")
            await asyncio.sleep(1)

    # Initialize the database
    models.Base.metadata.create_all(bind=database.engine)

    yield
