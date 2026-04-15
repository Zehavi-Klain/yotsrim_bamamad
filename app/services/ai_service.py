import os
import time
import random
import pdfkit
import requests
from pathlib import Path
from dotenv import load_dotenv
import json

load_dotenv()

class AIService:
    def __init__(self):
        raw_key = os.getenv("GEMINI_API_KEY", "")
        self.api_key = raw_key.replace('"', '').replace("'", "").replace(",", "").strip()
        self.wkhtml_path = os.getenv("WKHTML_PATH")
        
        self.base_dir = Path(__file__).parent.parent
        self.storage_dir = self.base_dir / "storage" / "created_by_ai"
        
        try:
            prompt_file = self.base_dir / "prompt.txt"
            with open(prompt_file, "r", encoding="utf-8") as f:
                self.prompt_template = f.read()
        except Exception:
            self.prompt_template = "Create a simple coloring page." 

        self.config = pdfkit.configuration(wkhtmltopdf=self.wkhtml_path)

    def get_random_existing_pdf(self):
        """פונקציית עזר למקרה של שגיאה - מחזירה קובץ קיים מהמאגר"""
        existing_files = list(self.storage_dir.glob("*.pdf"))
        if existing_files:
            chosen = random.choice(existing_files)
            return str(chosen)
        return None

    async def generate_ai_pdf(self):
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={self.api_key}"
            
            payload = {
                "contents": [{
                    "parts": [{"text": self.prompt_template.strip()}]
                }]
            }

            headers = {'Content-Type': 'application/json'}
            
            response = requests.post(
                url, 
                data=json.dumps(payload), 
                headers=headers, 
                timeout=45
            )
            
            if response.status_code != 200:
                return self.get_random_existing_pdf()

            data = response.json()
            html_content = data['candidates'][0]['content']['parts'][0]['text']
            html_content = html_content.replace("```html", "").replace("```", "").strip()

            file_name = f"ai_poster_{int(time.time())}.pdf"
            output_path = str(self.storage_dir / file_name)
            
            pdfkit.from_string(html_content, output_path, configuration=self.config)
            return output_path

        except Exception:
            return self.get_random_existing_pdf()