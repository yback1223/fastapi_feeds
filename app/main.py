import logging
import os
from fastapi import FastAPI
from logging.handlers import TimedRotatingFileHandler
from app.routes import router as feed_router
from app.database import engine, Base

app = FastAPI(
	title="Career Planner Feed API",
	version="1.0.0",
	docs_url="/swagger",
	redoc_url=None  # ReDoc 문서 비활성화
)

Base.metadata.create_all(bind=engine)

app.include_router(feed_router, prefix="/feeds")

