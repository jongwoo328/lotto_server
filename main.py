from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from router import v1

app = FastAPI(
    title='lotto API',
    version='1.0.0'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1.router)
