import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.logger import Logger
from app.settings import Settings
from app.router_description import tags_metadata

config = Settings()

log_dir = os.path.dirname(os.path.abspath(__file__)) + "/log/"
logger = Logger(log_dir=log_dir, log_level=logging.DEBUG)

app = FastAPI(openapi_tags=tags_metadata)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

from app.messages import messages

app.include_router(messages, prefix="/messages", tags=["Messages"])
