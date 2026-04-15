AI Workbook & Poster Generator
Overview
A backend system built with FastAPI for generating and retrieving educational PDF content.
The system supports both AI-generated posters and pre-made worksheets based on user input.
________________________________________
Features
•	Generate AI-based posters as PDF files
•	Retrieve pre-made worksheets based on age group and interests
•	Download files directly via API endpoints
•	Fallback mechanism to existing files in case of AI failure
•	Clean service-based architecture
________________________________________
Tech Stack
•	Python
•	FastAPI
•	PDFKit (wkhtmltopdf)
•	Requests
•	Environment Variables (.env)
________________________________________
API Endpoints
Generate AI Poster
POST /generate-ai-poster
Generates a PDF using AI and returns it for download.
________________________________________
Get Ready Workbook
POST /get-ready-workbook
Returns an existing worksheet PDF based on user input (age group and interests).
________________________________________
Project Structure
app/
•	main.py
•	services/
•	models/
•	storage/
________________________________________
How to Run
1.	Create virtual environment
python -m venv .venv
2.	Activate environment
..venv\Scripts\Activate.ps1
3.	Install dependencies
pip install -r requirements.txt
4.	Run the server
uvicorn app.main:app --reload
5.	Open in browser
http://127.0.0.1:8000/docs
________________________________________
Notes
•	.env file is required for API keys and configuration
•	Generated and stored files are not included in the repository
•	Some internal logic and data were omitted for security reasons
________________________________________
