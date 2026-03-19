import os
import time
import random
import pdfkit
import requests
from pathlib import Path
from dotenv import load_dotenv
import json

# טעינת המשתנים מקובץ .env
load_dotenv()

class AIService:
    def __init__(self):
        # קריאה מהקובץ הסודי (או ערך ברירת מחדל אם לא קיים)
        raw_key = os.getenv("GEMINI_API_KEY", "")
        self.api_key = raw_key.replace('"', '').replace("'", "").replace(",", "").strip()
        # self.prompt_template = os.getenv("PROMPT_TEMPLATE")
        self.wkhtml_path = os.getenv("WKHTML_PATH")
        
        # הגדרת נתיב ה-STORAGE בתוך תיקיית app
        self.base_dir = Path(__file__).parent.parent
        self.storage_dir = self.base_dir / "storage" / "creat_by_ai"
        
        # קריאת הפרומפט מקובץ הטקסט
        try:
            prompt_file = self.base_dir / "prompt.txt"
            with open(prompt_file, "r", encoding="utf-8") as f:
                self.prompt_template = f.read()
            print(">>> SUCCESS: Prompt loaded from file.")
        except Exception as e:
            print(f">>> ERROR: Could not read prompt.txt: {e}")
            self.prompt_template = "Create a simple coloring page." # גיבוי למקרה חירום

        self.config = pdfkit.configuration(wkhtmltopdf=self.wkhtml_path)

    def get_random_existing_pdf(self):
        """פונקציית עזר למקרה של שגיאה - מחזירה קובץ קיים מהמאגר"""
        existing_files = list(self.storage_dir.glob("*.pdf"))
        if existing_files:
            chosen = random.choice(existing_files)
            print(f">>> FALLBACK: Returning random existing file: {chosen.name}")
            return str(chosen)
        return None

    async def generate_ai_pdf(self):
        print(">>> STARTING AI PDF GENERATION...")
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={self.api_key}"
            
            # הדרך הכי בטוחה לעטוף טקסט ארוך ל-JSON
            payload = {
                "contents": [{
                    "parts": [{"text": self.prompt_template.strip()}]
                }]
            }

            headers = {'Content-Type': 'application/json'}
            
            # שליחה עם הדפסה של מה בדיוק אנחנו שולחים (לדיבאג)
            response = requests.post(
                url, 
                data=json.dumps(payload), # המרה בטוחה לטקסט JSON
                headers=headers, 
                verify=False, 
                timeout=45
            )
            
            if response.status_code != 200:
                # כאן אנחנו נראה בדיוק למה גוגל כועס
                print(f">>> GEMINI ERROR {response.status_code}!")
                print(f">>> DETAILED ERROR FROM GOOGLE: {response.text}")
                return self.get_random_existing_pdf()

            # ... המשך הקוד כרגיל ...
            data = response.json()
            html_content = data['candidates'][0]['content']['parts'][0]['text']
            html_content = html_content.replace("```html", "").replace("```", "").strip()

            file_name = f"ai_poster_{int(time.time())}.pdf"
            output_path = str(self.storage_dir / file_name)
            
            pdfkit.from_string(html_content, output_path, configuration=self.config)
            print(f">>> SUCCESS! Saved to: {output_path}")
            return output_path

        except Exception as e:
            print(f">>> CRITICAL ERROR: {str(e)}")
            return self.get_random_existing_pdf()