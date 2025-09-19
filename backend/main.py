
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import JSONResponse
from typing import List
import uvicorn
import os
import pdfplumber
from docx import Document
import sqlite3
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import spacy

app = FastAPI()

# Personalized recommendation based on extracted skills
def recommend_for_skills(skill_levels: dict):
    courses_conn = sqlite3.connect('data/courses.db')
    course_df = pd.read_sql_query('''
        SELECT c.course_id, c.course_name, cs.skill, cs.weight
        FROM courses c
        JOIN course_skills cs ON c.course_id = cs.course_id
    ''', courses_conn)
    course_matrix = course_df.pivot_table(index=['course_id','course_name'], columns='skill', values='weight', fill_value=0)
    all_skills = course_matrix.columns.tolist()
    # Build student vector from skill_levels (default 0 if not present)
    student_vector = [skill_levels.get(skill, 0) for skill in all_skills]
    similarity = cosine_similarity([student_vector], course_matrix.values)[0]
    recommendations = []
    for idx, course in enumerate(course_matrix.index):
        course_name = course[1]
        recommendations.append({
            "course_name": course_name,
            "score": round(similarity[idx], 3)
        })
    recommendations.sort(key=lambda x: x["score"], reverse=True)
    courses_conn.close()
    return recommendations

@app.post("/personalized-recommendations")
async def personalized_recommendations(request: Request):
    data = await request.json()
    skill_levels = data.get("skill_levels", {})
    recs = recommend_for_skills(skill_levels)
    return JSONResponse(content={"recommendations": recs})

# Skill extraction logic
SKILL_KEYWORDS = ["python", "aws", "cli", "networking", "docker", "linux", "git", "mlops", "devops",
    "java", "c++", "cloud", "azure", "gcp", "kubernetes", "terraform", "ansible",
    "sql", "nosql", "data science", "machine learning", "deep learning", "pandas",
    "numpy", "scikit-learn", "flask", "django", "rest api", "agile", "scrum"]

def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

# Improved name extraction using spaCy

nlp = spacy.load("en_core_web_sm")
def extract_name(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return "Unknown"

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return " ".join([para.text for para in doc.paragraphs])

def extract_skills(text):
    text = text.lower()
    return [skill for skill in SKILL_KEYWORDS if skill in text]

@app.post("/extract-skills/")
async def extract_skills_api(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())
    if file.filename.endswith(".pdf"):
        text = extract_text_from_pdf(temp_path)
    elif file.filename.endswith(".docx"):
        text = extract_text_from_docx(temp_path)
    else:
        os.remove(temp_path)
        return JSONResponse({"error": "Unsupported file type"}, status_code=400)
    os.remove(temp_path)
    name = extract_name(text)
    skills = extract_skills(text)
    return {"name": name, "skills": skills}

# Recommendation logic
def get_recommendations():
    students_conn = sqlite3.connect('data/students.db')
    courses_conn = sqlite3.connect('data/courses.db')
    student_df = pd.read_sql_query('''
        SELECT s.student_id, s.name, sk.skill, sk.level
        FROM students s
        JOIN student_skills sk ON s.student_id = sk.student_id
    ''', students_conn)
    course_df = pd.read_sql_query('''
        SELECT c.course_id, c.course_name, cs.skill, cs.weight
        FROM courses c
        JOIN course_skills cs ON c.course_id = cs.course_id
    ''', courses_conn)
    student_matrix = student_df.pivot_table(index=['student_id','name'], columns='skill', values='level', fill_value=0)
    course_matrix = course_df.pivot_table(index=['course_id','course_name'], columns='skill', values='weight', fill_value=0)
    student_matrix, course_matrix = student_matrix.align(course_matrix, join='outer', axis=1, fill_value=0)
    similarity = cosine_similarity(student_matrix, course_matrix)
    similarity_df = pd.DataFrame(similarity, index=student_matrix.index, columns=course_matrix.index)
    recommendations = {}
    for student in similarity_df.index:
        student_name = student[1]
        if student_name.lower() in ["alice", "bob"]:
            continue
        ranked = similarity_df.loc[student].sort_values(ascending=False)
        recommendations[student_name] = []
        for course_id, score in ranked.items():
            course_name = course_id[1]
            recommendations[student_name].append({
                "course_name": course_name,
                "score": round(score, 3)
            })
    students_conn.close()
    courses_conn.close()
    return recommendations

# Get recommendations for a specific student name
def get_recommendations_for_name(student_name):
    all_recs = get_recommendations()
    return all_recs.get(student_name, [])

@app.get("/recommendations/{student_name}")
def recommendations_for_name_api(student_name: str):
    recs = get_recommendations_for_name(student_name)
    return JSONResponse(content={"recommendations": recs})



if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
