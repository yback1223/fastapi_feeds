from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.schemas import FeedCreate, FeedResponse
from app.services import feed_service
from app.database import get_db
from app.services.storage_interface import StorageInterface  # Assuming you have this interface
from app.services.kt_cloud_storage import KTCloudStorage
from app.services.local_storage import LocalStorage
router = APIRouter()

def get_kt_storage() -> StorageInterface:
	return LocalStorage()

@router.get('/get', response_model=list[FeedResponse], status_code=status.HTTP_200_OK)
async def get_user_feeds(user_id: int = Query(...), db: Session = Depends(get_db)):
	try:
		feeds = await feed_service.get_user_feeds_service(db, user_id)
		if not feeds:
			return []
		return feeds
	except HTTPException as e:
		raise
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred while fetching the feeds: {e}")

@router.post('/create', response_model=list[FeedResponse], status_code=status.HTTP_201_CREATED)
async def create_feed(feed_data: FeedCreate, user_id: int = Query(...), db: Session = Depends(get_db), storage: StorageInterface = Depends(get_kt_storage)):
	try: 
		await feed_service.create_feed_service(db, feed_data, storage)
		feeds = await feed_service.get_user_feeds_service(db, user_id)
		return feeds
	except ValueError as e:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred while creating the feed. {e}")

@router.delete('/delete', status_code=status.HTTP_204_NO_CONTENT)
async def delete_feed(feed_id: int = Query(...), db: Session = Depends(get_db), storage: StorageInterface = Depends(get_kt_storage)):
	try:
		await feed_service.delete_feed_service(db, feed_id, storage)
	except ValueError as e:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while deleting the feed.")

@router.put('/update', response_model=FeedResponse, status_code=status.HTTP_200_OK)
async def update_feed(feed_id: int, feed_data: FeedCreate, db: Session = Depends(get_db), storage: StorageInterface = Depends(get_kt_storage)):
	try:
		updated_feed = await feed_service.update_feed_service(db, feed_id, feed_data, storage)
		return updated_feed
	except ValueError as e:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while updating the feed.")

# @router.get('/create/timelapse')
# async def update_feed(user_id: int, feed_data: FeedCreate, db: Session = Depends(get_db), storage: StorageInterface = Depends(get_kt_storage)):
# 	try:
# 		video_url = await feed_service.get_timelapse_url(db, user_id, storage)