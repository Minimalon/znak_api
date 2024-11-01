from fastapi import FastAPI
from auth.router import router as auth_router
import sys
from pathlib import Path


sys.path.append(Path(__file__).parent)

app = FastAPI()


app.include_router(auth_router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='10.8.16.18', port=8180)