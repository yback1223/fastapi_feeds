from pydantic import BaseModel, Field
from typing import List, Dict
from datetime import datetime

class FeedCreate(BaseModel):
	title: str = Field(..., max_length=255)
	content: str
	hashtags: List[Dict]  # JSON 리스트로 받음
	date: Dict  # JSON 객체로 받음
	user_id: int

class FeedResponse(BaseModel):
	id: int
	title: str
	content: str
	hashtags: List[Dict]  # JSON 리스트로 반환
	date: Dict  # JSON 객체로 반환
	created_at: datetime
	image_url: str
	user_id: int

	class Config:
		orm_mode = True  # ORM 객체를 Pydantic 모델로 자동 변환
