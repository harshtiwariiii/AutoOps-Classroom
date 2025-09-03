import streamlit as st

st.title("AutoOps Classroom: Skill Extractor & Course Recommender")

if uploaded_file := st.file_uploader("Upload your CV (PDF or DOCX)", type=["pdf", "docx"]):
    st.success("CV uploaded successfully!")
    # Placeholder for skill extraction
    st.write("Extracted Skills: Python, AWS, CLI, Networking")
    # Placeholder for course recommendations
    st.write("Suggested Courses:")
    st.write("1. AWS Basics")
    st.write("2. DevOps Advanced")
    st.write("3. MLOps Specialization")

st.info("This is a basic frontend. Backend integration and real skill extraction will be added later.")
