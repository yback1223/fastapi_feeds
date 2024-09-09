import requests
import boto3
import os
import time
from typing import Any
from botocore.exceptions import NoCredentialsError, ClientError
from .storage_interface import StorageInterface
from dotenv import load_dotenv
from ..config import FeedLogger

load_dotenv()

logger = FeedLogger().get_logger()

class ImageService:
	def __init__(self, storage: StorageInterface):
		self.storage = storage
		self.headers = {
				"authorization": f"Bearer {os.getenv('STABILITY_AI_API_KEY')}",
				"accept": "image/*"
			},

	async def generate_image(self, content: str) -> str:
		image_bytes: bytes | Any = await self.get_stability_ai_image_bytes(content)
		return image_bytes

	async def save_image(self, user_id: int, title: str, image_bytes: str):
		file_path = f'images/{user_id}/{title}.png'
		image_url = await self.storage.upload_image_from_storage(image_bytes, file_path)
		return image_url
	
	async def delete_image(self, file_path: str) -> bool:
		return await self.storage.delete_image_from_storage(file_path)

	async def get_stability_ai_image_bytes(self, content: str) -> bytes | Any:
		response = await requests.post(
			f"https://api.stability.ai/v2beta/stable-image/generate/ultra",
			headers=self.headers,
			files={"none": ''},
			data={
				"prompt": content,
				"output_format": "png",
			},
		)

		if response.status_code == 200:
			# with open("./5.webp", 'wb') as file:
			# 	file.write(response.content)
			return response.content
		else:
			raise Exception(str(response.json()))