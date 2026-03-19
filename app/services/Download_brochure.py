import os

class StorageService:
    def __init__(self):
        self.base_path = os.path.join(os.getcwd(),"app", "storage")
    def get_workbook_from_storage(self, age_group: str, interest: str):
        file_name = f"{interest}.pdf" 
        
        file_path = os.path.join(self.base_path, age_group, file_name)
        if os.path.exists(file_path):
            print(f"DEBUG: SUCCESS! File found.")
            return file_path
        return None


