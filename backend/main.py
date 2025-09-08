# Backend entry point
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import uvicorn
import os

# For PDF and DOCX extraction
import pdfplumber
from docx import Document

app = FastAPI()

# Define skill keywords
SKILL_KEYWORDS = ["python", "aws", "cli", "networking", "docker", "linux", "git", "mlops", "devops"]

def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return " ".join([para.text for para in doc.paragraphs])

def extract_skills(text):
    text = text.lower()
    found_skills = [skill for skill in SKILL_KEYWORDS if skill in text]
    return found_skills

@app.post("/extract-skills/")
async def extract_skills_api(file: UploadFile = File(...)):
    # Save uploaded file temporarily
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    # Extract text
    if file.filename.endswith(".pdf"):
        text = extract_text_from_pdf(temp_path)
    elif file.filename.endswith(".docx"):
        text = extract_text_from_docx(temp_path)
    else:
        os.remove(temp_path)
        return JSONResponse({"error": "Unsupported file type"}, status_code=400)

    os.remove(temp_path)
    skills = extract_skills(text)
    return {"skills": skills}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
