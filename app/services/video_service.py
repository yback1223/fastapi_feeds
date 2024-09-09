import requests, os
from typing import List
from dotenv import load_dotenv
from ..config import FeedLogger
from .storage_interface import StorageInterface

logger = FeedLogger().get_logger()

load_dotenv()

VIDEO_CREATING = 0

class VideoService:
	def __init__(self, storage: StorageInterface):
		self.storage = storage
		self.api_url = "https://api.stability.ai/v2beta/image-to-video"
		self.request_headers = {
			"authorization": f"Bearer {os.getenv('STABILITY_AI_API_KEY')}"
		}
		self.fetch_headers = {
			'accept': "video/*",
			"authorization": f"Bearer {os.getenv('STABILITY_AI_API_KEY')}"
		}

	def get_video_pid(self, file_paths: List[str]) -> str:
		try:
			files = [('image', open(file, 'rb')) for file in file_paths]

			response = requests.post(
				self.api_url,
				headers=self.request_headers,
				files=files,
				data={
					"seed": 0,
					"cfg_scale": 1.8,
					"motion_bucket_id": 127
				},
			)
			response.raise_for_status()

			pid = response.json().get('id')
			if pid:
				return pid
			else:
				raise Exception("No PID found in the response.")
		except Exception as e:
			logger.critical(f"Error during video creation: {e}")
		finally:
			for file in files:
				file[1].close()

	def fetch_video_result(self, pid: str, output_file: str = "video.mp4"):
		try:
			response = requests.get(
				f"{self.api_url}/result/{pid}",
				headers=self.fetch_headers
			)

			if response.status_code == 202:
				return VIDEO_CREATING
			elif response.status_code == 200:
				# with open(output_file, 'wb') as file:
				# 	file.write(response.content)
				# return output_file
				return response.content
			else:
				logger.error(f"Error: {response.json()}")
				return -1
		except Exception as e:
			logger.critical(f"Error fetching video result: {e}")

	async def save_video(self, user_id: int, title: str, image_bytes: str):
		file_path = f'videos/{user_id}/{title}.png'
		image_url = await self.storage.upload_file_from_storage(image_bytes, file_path)
		return image_url
	
	async def delete_video(self, file_path: str) -> bool:
		return await self.storage.delete_file_from_storage(file_path)