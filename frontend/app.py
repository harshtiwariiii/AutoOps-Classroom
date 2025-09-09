import streamlit as st
import requests

st.title("AutoOps Classroom: Skill Extractor & Course Recommender")

extract_url = "http://127.0.0.1:8000/extract-skills/"
personalized_url = "http://127.0.0.1:8000/personalized-recommendations"
recommend_url = "http://127.0.0.1:8000/recommendations"

uploaded_file = st.file_uploader("Upload your CV (PDF or DOCX)", type=["pdf", "docx"])

if uploaded_file:
    st.success("CV uploaded successfully!")
    files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
    try:
        response = requests.post(extract_url, files=files)
        if response.status_code == 200:
            data = response.json()
            name = data.get("name", "Unknown")
            skills = data.get("skills", [])
            st.write(f"Extracted Name: {name}")
            st.write(f"Extracted Skills: {', '.join(skills) if skills else 'None found'}")
            # Get recommendations for this name
            rec_url = f"http://127.0.0.1:8000/recommendations/{name}"
            rec_response = requests.get(rec_url)
            if rec_response.status_code == 200:
                recs = rec_response.json().get("recommendations", [])
                st.header(f"Course Recommendations for {name}:")
                for course in recs:
                    st.write(f"{course['course_name']}: {course['score']}")
            else:
                st.error("Could not fetch recommendations for this name.")
        else:
            st.error(f"Error: {response.json().get('error', 'Unknown error')}")
    except Exception as e:
        st.error(f"Failed to connect to backend: {e}")

st.header("Course Recommendations for All Students")
try:
    rec_response = requests.get(recommend_url)
    if rec_response.status_code == 200:
        recommendations = rec_response.json()
        for student, courses in recommendations.items():
            st.subheader(f"Recommendations for {student}:")
            for course in courses:
                st.write(f"{course['course_name']}: {course['score']}")
    else:
        st.error("Could not fetch recommendations.")
except Exception as e:
    st.error(f"Failed to connect to backend for recommendations: {e}")

st.info("Upload your CV to extract skills and see personalized course recommendations.")