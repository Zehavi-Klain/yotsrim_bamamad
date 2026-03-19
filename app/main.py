from fastapi import FastAPI,Response
from app.models.request_model_from_user import WorkbookRequest # ייבוא המודל שיצרת
from fastapi.responses import FileResponse # חובה בשביל לשלוח קבצים
from app.services.Download_brochure import StorageService # ייבוא הסרויס מהקובץ שלך
from datetime import datetime
from app.services.ai_service import AIService
import os
from fastapi.responses import FileResponse

app = FastAPI(title="מחולל חוברות עבודה")
storage_service_instance = StorageService()

@app.post("/generate-ai-poster")
async def generate_ai_poster():
    # ה-Import והיצירה קורים רק כשלוחצים על הכפתור!
    try:
        from app.services.ai_service import AIService
        service = AIService()
        file_path = await service.generate_ai_pdf()
        
        if file_path and os.path.exists(file_path):
            return FileResponse(
            path=file_path, 
            filename="my_poster.pdf", 
            media_type='application/pdf'
        )
        
    except Exception as e:
        print(f"Detailed Error: {e}")
        return {"error": str(e)}
    
    return {"error": "Failed to generate file"}


@app.post("/get-ready-workbook")
async def get_ready(request: WorkbookRequest):
    age_val = request.age_group.value
    interest_val = request.Interests.value
    file_path = storage_service_instance.get_workbook_from_storage(age_val,interest_val)
    if file_path:
        return FileResponse(file_path, media_type='application/pdf', filename=f"workbook_{interest_val}.pdf")
    
    return {"error": "מצטערים, החוברת המבוקשת לא נמצאה במאגר"}

@app.post("/generate")
async def generate_workbook(request: WorkbookRequest):
    return {
        "message": f"הבקשה התקבלה! יוצר חוברת לגיל {request.age_group.value}",
        "data": request
    }