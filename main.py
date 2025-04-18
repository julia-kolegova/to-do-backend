import os
import uvicorn

from dotenv import load_dotenv

if os.path.exists('.env'):
    load_dotenv('.env')

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_sqlalchemy import DBSessionMiddleware

from common.settings import settings
from app.api.routers import api_router


app = FastAPI(openapi_prefix="/api")

app.add_middleware(
    DBSessionMiddleware,
    db_url=settings.sql_alchemy_connection_url,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run(app, port=settings.port)
