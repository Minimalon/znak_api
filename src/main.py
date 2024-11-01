from fastapi import FastAPI
from auth.router import router as auth_router
import sys
from pathlib import Path


sys.path.append(Path(__file__).parent)

app = FastAPI()


app.include_router(auth_router)