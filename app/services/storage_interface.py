from abc import ABC, abstractmethod

class StorageInterface(ABC):
	@abstractmethod
	async def upload_image_from_storage(self, file_bytes: bytes, file_path: str) -> str:
		pass

	@abstractmethod
	async def delete_image_from_storage(self, file_path: str) -> bool:
		pass
