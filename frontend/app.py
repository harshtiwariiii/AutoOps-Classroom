import streamlit as st
import requests

st.title("AutoOps Classroom: Skill Extractor & Course Recommender")

backend_url = "http://127.0.0.1:8000/extract-skills/"

uploaded_file = st.file_uploader("Upload your CV (PDF or DOCX)", type=["pdf", "docx"])

if uploaded_file:
    st.success("CV uploaded successfully!")
    files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
    try:
        response = requests.post(backend_url, files=files)
        if response.status_code == 200:
            skills = response.json().get("skills", [])
            st.write(f"Extracted Skills: {', '.join(skills) if skills else 'None found'}")
            # Placeholder for course recommendations
            st.write("Suggested Courses:")
            st.write("1. AWS Basics")
            st.write("2. DevOps Advanced")
            st.write("3. MLOps Specialization")
        else:
            st.error(f"Error: {response.json().get('error', 'Unknown error')}")
    except Exception as e:
        st.error(f"Failed to connect to backend: {e}")

st.info("Upload your CV to extract skills and get course recommendations.")
