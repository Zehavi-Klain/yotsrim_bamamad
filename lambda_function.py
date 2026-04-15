import sys
import os

# מוודא ש-Lambda תוכל למצוא את תיקיית app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.main import app  # מייבא את האובייקט app מקובץ ה-main שלך
from mangum import Mangum

# זהו ה-Handler ש-AWS מחפשת
handler = Mangum(app, lifespan="off")