from sqlalchemy.orm import Session
from app.models import Feed
from app.schemas import FeedCreate
from sqlalchemy.exc import SQLAlchemyError
from .config import FeedLogger

logger = FeedLogger().get_logger()

async def create_feed(db: Session, feed_data: FeedCreate, image_url: str):
	try:
		new_feed = Feed(
			title=feed_data.title,
			content=feed_data.content,
            hashtags=feed_data.hashtags,
            date=feed_data.date, 
			image_url=image_url,
			user_id=feed_data.user_id,
		)
		db.add(new_feed)
		db.commit()
		db.refresh(new_feed)
		logger.info(f"Feed created successfully for user_id: {feed_data.user_id}")
		return new_feed
	except SQLAlchemyError as e:
		db.rollback()
		logger.error(f"Database error during feed creation for user_id {feed_data.user_id}: {e}")
		raise Exception("Feed creation failed due to a database error.")
	except Exception as e:
		logger.critical(f"Unexpected error during feed creation for user_id {feed_data.user_id}: {e}")
		raise

async def get_feeds_by_user(db: Session, user_id: int):
	try:
		feeds = db.query(Feed).filter(Feed.user_id == user_id).all()
		if feeds:
			logger.info(f"Feeds retrieved successfully for user_id: {user_id}")
		else:
			logger.warning(f"No feeds found for user_id {user_id}")
		return feeds
	except SQLAlchemyError as e:
		logger.error(f"Database error during feed retrieval for user_id {user_id}: {e}")
		raise Exception("Feed retrieval failed due to a database error.", e)
	except Exception as e:
		logger.critical(f"Unexpected error during feed retrieval for user_id {user_id}: {e}")
		raise

async def get_feed_by_id(db: Session, feed_id: int):
	try:
		feed = db.query(Feed).filter(Feed.id == feed_id).first()
		if feed:
			logger.info(f"Feed retrieved successfully with feed_id: {feed_id}")
		else:
			logger.warning(f"Feed with feed_id {feed_id} not found.")
		return feed
	except SQLAlchemyError as e:
		logger.error(f"Database error during feed retrieval with feed_id {feed_id}: {e}")
		raise Exception("Feed retrieval failed due to a database error.")
	except Exception as e:
		logger.critical(f"Unexpected error during feed retrieval with feed_id {feed_id}: {e}")
		raise

async def delete_feed(db: Session, feed_id: int):
	try:
		feed = db.query(Feed).filter(Feed.id == feed_id).first()
		if feed:
			db.delete(feed)
			db.commit()
			logger.info(f"Feed deleted successfully with feed_id: {feed_id}")
			return True
		else:
			logger.warning(f"Feed with feed_id {feed_id} not found.")
			return False
	except SQLAlchemyError as e:
		db.rollback()
		logger.error(f"Database error during feed deletion with feed_id {feed_id}: {e}")
		raise Exception("Feed deletion failed due to a database error.")
	except Exception as e:
		logger.critical(f"Unexpected error during feed deletion with feed_id {feed_id}: {e}")
		raise

# Update an existing feed
async def update_feed(db: Session, feed_id: int, feed_data: FeedCreate, new_image_url: str):
	try:
		feed = db.query(Feed).filter(Feed.id == feed_id).first()
		if feed:
			feed.title = feed_data.title
			feed.content = feed_data.content
			feed.hashtags = feed_data.hashtags
			feed.date = feed_data.date
			feed.image_url = new_image_url
			db.commit()
			db.refresh(feed)
			logger.info(f"Feed updated successfully with feed_id: {feed_id}")
			return feed
		else:
			logger.warning(f"Feed with feed_id {feed_id} not found for update.")
			return None
	except SQLAlchemyError as e:
		db.rollback()
		logger.error(f"Database error during feed update with feed_id {feed_id}: {e}")
		raise Exception("Feed update failed due to a database error.")
	except Exception as e:
		logger.critical(f"Unexpected error during feed update with feed_id {feed_id}: {e}")
		raise