import asyncio

from fastapi import FastAPI
from src.auth.router import router as auth_router
from src.loggers import create_loggers

# Создание логгеров
asyncio.run(create_loggers())

app = FastAPI()

app.include_router(auth_router)

