import os
from pathlib import Path


class StorageService:
    def __init__(self):
        self.base_path = Path(__file__).parent.parent / "storage"
    def get_workbook_from_storage(self, age_group: str, interest: str):
        file_name = f"{interest}.pdf" 
        
        file_path = os.path.join(self.base_path, age_group, file_name)
        if os.path.exists(file_path):
            return file_path
        return None


