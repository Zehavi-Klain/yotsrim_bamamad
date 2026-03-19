import os
import time
import pdfkit
import google.generativeai as genai

class AIService:
    def __init__(self):
        # המפתח שלך ישירות - בלי os.getenv כרגע כדי למנוע טעויות
        self.api_key = "AIzaSyB0jLhurKlQUzFQcvvAR4JmoaW9jK9xsjs"
        self.wkhtml_path = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
        
        # הגדרה קריטית לנטפרי: מכריחים עבודה ב-REST
        genai.configure(api_key=self.api_key, transport='rest')
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        try:
            self.config = pdfkit.configuration(wkhtmltopdf=self.wkhtml_path)
        except:
            self.config = None
        
        print("DEBUG: Service is initialized with REST transport")

    async def generate_ai_pdf(self):
        print(">>> STARTING...")
        try:
            # פרומפט קצרצר רק כדי לראות שזה עובר את נטפרי
            print(">>> Sending to Gemini (REST)...")
            response = self.model.generate_content("Return only <h1>Success</h1>")
            
            # בדיקה אם קיבלנו תשובה
            if not response or not response.text:
                print(">>> Gemini returned empty response")
                return None
                
            html_code = response.text.strip()
            print(f">>> Gemini said: {html_code}")

            # יצירת הקובץ
            output_dir = os.path.join("storage", "creat_by_ai")
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, f"test_{int(time.time())}.pdf")

            print(">>> Creating PDF...")
            pdfkit.from_string(html_code, output_path, configuration=self.config)
            
            print(f">>> PDF DONE: {output_path}")
            return output_path

        except Exception as e:
            print(f">>> ERROR: {str(e)}")
            return None