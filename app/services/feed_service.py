from sqlalchemy.orm import Session
from app import crud
from app.schemas import FeedCreate
from .image_service import ImageService
from .video_service import VideoService
from .storage_interface import StorageInterface

IMAGE_AI = False
VIDEO_AI = False

async def create_feed_service(db: Session, feed_data: FeedCreate, storage: StorageInterface):
	image_service = ImageService(storage)
	if IMAGE_AI:
		image_url = create_image_service(feed_data, storage)
	else:
		image_url = 'test/image.png'

	new_feed = await crud.create_feed(db, feed_data, image_url)
	return new_feed

async def create_image_service(feed_data: FeedCreate, storage: StorageInterface):
	image_service = ImageService(storage)
	image_bytes = await image_service.generate_image(feed_data.content)
	if not image_bytes:
		raise ValueError("Image generation failed")

	image_url = await image_service.save_image(feed_data.user_id, feed_data.title, image_bytes)
	if not image_url:
		raise ValueError("Image saving failed")
	return image_url

async def get_user_feeds_service(db: Session, user_id: int):
	return await crud.get_feeds_by_user(db, user_id)

async def delete_feed_service(db: Session, feed_id: int, storage: StorageInterface):
	feed = await crud.get_feed_by_id(db, feed_id)
	if not feed:
		raise ValueError("Feed not found")

	if IMAGE_AI:
		image_service = ImageService(storage)
		
		if feed.image_url:
			await image_service.delete_image(feed.image_url)
	
	success = await crud.delete_feed(db, feed_id)
	if not success:
		raise ValueError("Feed not found or couldn't be deleted")

async def update_feed_service(db: Session, feed_id: int, feed_data: FeedCreate, storage: StorageInterface):
	existing_feed = await crud.get_feed_by_id(db, feed_id)
	if not existing_feed:
		raise ValueError('Feed not found')

	if IMAGE_AI:
		image_service = ImageService(storage)

		if existing_feed.image_url:
			await image_service.delete_image(existing_feed.image_url)

		new_image_bytes = await image_service.generate_image(feed_data.content)
		if not new_image_bytes:
			raise ValueError("New image generation failed")

		new_image_url = await image_service.save_image(feed_data.user_id, feed_data.title, new_image_bytes)
	else:
		new_image_url = 'test/new_image.png'

	updated_feed = await crud.update_feed(db, feed_id, feed_data, new_image_url)
	return updated_feed

async def get_timelapse_url(db: Session, user_id: int, storage: StorageInterface):
	user_feeds = await crud.get_feeds_by_user(db, user_id)
	image_urls = [image_url for image_url in user_feeds.image_url]
	if VIDEO_AI:
		video_service = VideoService(storage)

		video_bytes = await video_service.get_video_pid(image_urls)
		await video_service
