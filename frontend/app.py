
import streamlit as st
import requests


# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Add Course"])

if page == "Add Course":
    st.title("Add a New Course")
    course_name = st.text_input("Course Name")
    course_details = st.text_area("Course Details")
    video_file = st.file_uploader("Upload Course Video", type=["mp4", "mov", "avi"])

    # Dynamic modules, topics, subtopics
    if "modules" not in st.session_state:
        st.session_state.modules = []
    num_modules = st.number_input("Number of Modules", min_value=1, max_value=10, value=len(st.session_state.modules) or 1)
    while len(st.session_state.modules) < num_modules:
        st.session_state.modules.append({"name": "", "topics": []})
    while len(st.session_state.modules) > num_modules:
        st.session_state.modules.pop()

    for m_idx, module in enumerate(st.session_state.modules):
        st.subheader(f"Module {m_idx+1}")
        module["name"] = st.text_input(f"Module Name {m_idx+1}", value=module["name"], key=f"modname{m_idx}")
        num_topics = st.number_input(f"Number of Topics in Module {m_idx+1}", min_value=1, max_value=10, value=len(module["topics"]) or 1, key=f"numtopics{m_idx}")
        while len(module["topics"]) < num_topics:
            module["topics"].append({"name": "", "subtopics": []})
        while len(module["topics"]) > num_topics:
            module["topics"].pop()
        for t_idx, topic in enumerate(module["topics"]):
            topic["name"] = st.text_input(f"Topic Name {m_idx+1}-{t_idx+1}", value=topic["name"], key=f"topicname{m_idx}-{t_idx}")
            num_subtopics = st.number_input(f"Number of Subtopics in Topic {m_idx+1}-{t_idx+1}", min_value=1, max_value=10, value=len(topic["subtopics"]) or 1, key=f"numsubtopics{m_idx}-{t_idx}")
            while len(topic["subtopics"]) < num_subtopics:
                topic["subtopics"].append("")
            while len(topic["subtopics"]) > num_subtopics:
                topic["subtopics"].pop()
            for s_idx in range(num_subtopics):
                topic["subtopics"][s_idx] = st.text_input(f"Subtopic Name {m_idx+1}-{t_idx+1}-{s_idx+1}", value=topic["subtopics"][s_idx], key=f"subtopic{m_idx}-{t_idx}-{s_idx}")

    if st.button("Submit Course"):
        course_data = {
            "course_name": course_name,
            "course_details": course_details,
            "video_file": video_file.name if video_file else None,
            "modules": st.session_state.modules
        }
        st.success(f"Course '{course_name}' added!")
        st.json(course_data)
    st.stop()

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
            st.subheader("Detected skills (edit levels 1–10):")
            skill_levels = {}
            cols = st.columns(2)
            for idx, skill in enumerate(skills):
                with cols[idx % 2]:
                    skill_levels[skill] = st.slider(skill, 1, 10, 1)
            if st.button("Get Personalized Recommendations"):
                payload = {"skill_levels": skill_levels}
                rec_response = requests.post(personalized_url, json=payload)
                if rec_response.status_code == 200:
                    recs = rec_response.json().get("recommendations", [])
                    st.header(f"Course Recommendations for {name}:")
                    for course in recs:
                        st.write(f"{course['course_name']}: {course['score']}")
                else:
                    st.error("Could not fetch personalized recommendations.")
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