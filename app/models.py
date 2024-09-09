from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, func
from app.database import Base

class Feed(Base):
	__tablename__ = "feeds"

	id = Column(Integer, primary_key=True, index=True)
	title = Column(String(255), nullable=False)
	content = Column(Text, nullable=False)
	hashtags = Column(JSON, nullable=True)
	date = Column(JSON, nullable=True)
	created_at = Column(DateTime, server_default=func.now())
	image_url = Column(String(500), nullable=True)
	user_id = Column(Integer, index=False)

class Video(Base):
	__tablename__ = "videos"

	id = Column(Integer, primary_key=True, index=True)
	user_id = Column(Integer, index=True, nullable=False)
	video_url = Column(String(500), nullable=False)
	description = Column(Text, nullable=True)
	