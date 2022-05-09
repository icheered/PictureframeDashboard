import os

import dotenv
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse

from api.api import api_router

dotenv.load_dotenv()



app = FastAPI(title="Backend API")

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    """Perform some logic on startup"""
    pass


@app.on_event("shutdown")
def shutdown():
    """Perform some logic on shutdown"""
    pass


app.include_router(
    api_router,
)

@app.get("/")
async def read_index():
    return FileResponse('index.html')

@app.get("/style.css")
async def read_index():
    return FileResponse('style.css')


if __name__ == "__main__":
    uvicorn.run("main:app", host=os.environ.get('backend_host'), port=int(os.environ.get('backend_port')), reload=True)
