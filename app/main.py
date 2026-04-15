from fastapi import FastAPI,Response
from app.models.request_model_from_user import WorkbookRequest 
from fastapi.responses import FileResponse
from app.services.download_brochure import StorageService 
from datetime import datetime
from app.services.ai_service import AIService
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="מחולל חוברות עבודה")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

storage_service_instance = StorageService()

@app.post("/generate-ai-poster")
async def generate_ai_poster():
    try:
        service = AIService()
        file_path = await service.generate_ai_pdf()
        
        if file_path and os.path.exists(file_path):
            return FileResponse(
            path=file_path, 
            filename="my_poster.pdf", 
            media_type='application/pdf'
        )
        
    except Exception:
        return {"error": "Internal server error"}
    
    return {"error": "Failed to generate file"}


@app.post("/get-ready-workbook")
async def get_ready(request: WorkbookRequest):
    age_val = request.age_group.value
    interest_val = request.interests.value
    file_path = storage_service_instance.get_workbook_from_storage(age_val,interest_val)
    if file_path:
        return FileResponse(file_path, media_type='application/pdf', filename=f"workbook_{interest_val}.pdf")
    
    return {"error": "מצטערים, החוברת המבוקשת לא נמצאה במאגר"}

