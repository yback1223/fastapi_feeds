# KT Cloud Object Storage의 경우, 라이브러리나 API에 맞는 코드를 작성해야 합니다.
import requests
import os
from ..config import FeedLogger
from .storage_interface import StorageInterface

logger = FeedLogger().get_logger()

class KTCloudStorage(StorageInterface):
	def __init__(self):
		self.KT_ACCESS_KEY = os.getenv('KT_ACCESS_KEY')
		self.KT_SECRET_KEY = os.getenv('KT_SECRET_KEY')
		self.KT_BUCKET = os.getenv('KT_BUCKET')

	async def upload_file_from_storage(self, file_bytes: bytes, file_path: str) -> str:
		# KT Cloud Object Storage API 사용 예시
		try:
			response = requests.put(
				f"https://api.ktcloud.com/storage/v1/{self.KT_BUCKET}/{file_path}",
				headers={
					"Authorization": f"Bearer {self.KT_ACCESS_KEY}",
					"Content-Type": "image/webp"
				},
				data=file_bytes
			)
			response.raise_for_status()
			image_url = f"https://{self.KT_BUCKET}.ktcloud.com/{file_path}"
			logger.info(f"Image successfully uploaded to KT Cloud: {image_url}")
			return image_url
		except requests.RequestException as e:
			logger.error(f"Error occurred during KT Cloud upload: {e}")
			raise

	async def delete_file_from_storage(self, file_path: str) -> bool:
		try:
			response = requests.delete(
				f"https://api.ktcloud.com/storage/v1/{self.KT_BUCKET}/{file_path}",
				headers={"Authorization": f"Bearer {self.KT_ACCESS_KEY}"}
			)
			response.raise_for_status()
			logger.info(f"Image successfully deleted from KT Cloud: {file_path}")
			return True
		except requests.RequestException as e:
			logger.error(f"Error occurred during KT Cloud deletion: {e}")
			return False
