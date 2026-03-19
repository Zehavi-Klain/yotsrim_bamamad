from pydantic import BaseModel
from enum import Enum

class AgeGroup(str, Enum):
    YOUNG = "young"   # הערך שבאמת עובר בקוד
    MIDDLE = "middle"
    OLDER = "older"

class Interest(str,Enum):
    THINKING = "thinking"
    COLORING = "coloring"

class WorkbookRequest(BaseModel):
    age_group:AgeGroup
    Interests:Interest

    