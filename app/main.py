import logging
import os
from fastapi import FastAPI
from logging.handlers import TimedRotatingFileHandler
from app.routes import router as feed_router
from app.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
	title="Career Planner Feed API",
	version="1.0.0",
	docs_url="/swagger",
	redoc_url=None  # ReDoc 문서 비활성화
)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 출처 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용 (GET, POST, PUT, DELETE 등)
    allow_headers=["*"],  # 모든 헤더 허용
)

Base.metadata.create_all(bind=engine)

app.include_router(feed_router, prefix="/feeds")

