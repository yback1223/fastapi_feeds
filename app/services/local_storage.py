import os
from .storage_interface import StorageInterface

class LocalStorage(StorageInterface):
    def __init__(self, base_dir: str = 'media_files'):
        self.base_dir = base_dir
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

    async def upload_file_from_storage(self, image_bytes: bytes, file_path: str) -> str:
        full_path = os.path.join(self.base_dir, file_path)
        directory = os.path.dirname(full_path)

        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(full_path, 'wb') as file:
            file.write(image_bytes)

        return full_path

    async def delete_file_from_storage(self, file_path: str) -> bool:
        full_path = os.path.join(self.base_dir, file_path)
        if os.path.exists(full_path):
            os.remove(full_path)
            return True
        return False
