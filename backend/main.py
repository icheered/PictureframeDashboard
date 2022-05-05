import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.api import api_router

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

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=7001, reload=True)