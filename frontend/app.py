
import streamlit as st
import requests


# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Add Course", "View Courses"])

if page == "View Courses":
    st.title("📚 All Submitted Courses")
    
    if "submitted_courses" not in st.session_state:
        st.session_state["submitted_courses"] = []
    
    # Add sample courses if none exist
    if not st.session_state["submitted_courses"]:
        if st.button("📚 Add Sample Courses"):
            sample_courses = [
                {
                    "course_name": "Python Programming Masterclass",
                    "course_details": "Complete Python programming course covering fundamentals, data structures, algorithms, and advanced concepts. Perfect for beginners and intermediate developers.",
                    "video_file": "python_masterclass.mp4",
                    "modules": [
                        {
                            "name": "Python Fundamentals",
                            "description": "Learn the basics of Python programming language",
                            "topics": [
                                {
                                    "name": "Variables and Data Types",
                                    "description": "Understanding different data types in Python",
                                    "subtopics": ["Strings", "Numbers", "Lists", "Dictionaries", "Tuples"]
                                },
                                {
                                    "name": "Control Structures",
                                    "description": "Conditional statements and loops",
                                    "subtopics": ["If-else statements", "For loops", "While loops", "Break and Continue"]
                                }
                            ]
                        },
                        {
                            "name": "Object-Oriented Programming",
                            "description": "Learn OOP concepts in Python",
                            "topics": [
                                {
                                    "name": "Classes and Objects",
                                    "description": "Creating and using classes",
                                    "subtopics": ["Class definition", "Object creation", "Methods", "Attributes"]
                                }
                            ]
                        }
                    ]
                },
                {
                    "course_name": "AWS Cloud Computing",
                    "course_details": "Comprehensive AWS course covering EC2, S3, RDS, Lambda, and other essential AWS services for cloud computing.",
                    "video_file": "aws_cloud.mp4",
                    "modules": [
                        {
                            "name": "AWS Fundamentals",
                            "description": "Introduction to AWS cloud platform",
                            "topics": [
                                {
                                    "name": "AWS Services Overview",
                                    "description": "Understanding AWS service categories",
                                    "subtopics": ["Compute services", "Storage services", "Database services", "Networking"]
                                }
                            ]
                        }
                    ]
                }
            ]
            st.session_state["submitted_courses"] = sample_courses
            st.success("Sample courses added!")
            st.rerun()
    
    if not st.session_state["submitted_courses"]:
        st.info("No courses submitted yet.")
    else:
        # Create columns for course cards
        cols = st.columns(2)
        
        for idx, course in enumerate(st.session_state["submitted_courses"]):
            with cols[idx % 2]:
                # Course Card
                with st.container():
                    st.markdown("""
                    <div style="
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        padding: 20px;
                        border-radius: 15px;
                        margin: 10px 0;
                        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
                        color: white;
                        border: 1px solid rgba(255,255,255,0.2);
                    ">
                    """, unsafe_allow_html=True)
                    
                    # Course Image placeholder
                    st.markdown("""
                    <div style="text-align: center; margin-bottom: 15px;">
                        <div style="
                            width: 100%;
                            height: 150px;
                            background: rgba(255,255,255,0.1);
                            border-radius: 10px;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            font-size: 48px;
                            margin-bottom: 10px;
                        ">
                            📖
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Course Title
                    st.markdown(f"""
                    <h3 style="
                        color: white;
                        text-align: center;
                        margin: 0 0 10px 0;
                        font-size: 1.5em;
                        font-weight: bold;
                    ">{course['course_name']}</h3>
                    """, unsafe_allow_html=True)
                    
                    # Course Details Preview
                    details_preview = course['course_details'][:100] + "..." if len(course['course_details']) > 100 else course['course_details']
                    st.markdown(f"""
                    <p style="
                        color: rgba(255,255,255,0.9);
                        text-align: center;
                        margin: 0 0 15px 0;
                        font-size: 0.9em;
                        line-height: 1.4;
                    ">{details_preview}</p>
                    """, unsafe_allow_html=True)
                    
                    # Video indicator
                    if course['video_file']:
                        st.markdown("""
                        <div style="text-align: center; margin-bottom: 10px;">
                            <span style="
                                background: rgba(255,255,255,0.2);
                                padding: 5px 10px;
                                border-radius: 20px;
                                font-size: 0.8em;
                            ">🎥 Video Available</span>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Modules count
                    modules_count = len(course['modules'])
                    st.markdown(f"""
                    <div style="text-align: center; margin-bottom: 15px;">
                        <span style="
                            background: rgba(255,255,255,0.2);
                            padding: 5px 10px;
                            border-radius: 20px;
                            font-size: 0.8em;
                        ">📚 {modules_count} Module{'s' if modules_count != 1 else ''}</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Course Details Button
                    if st.button(f"View Details", key=f"view_{idx}", use_container_width=True):
                        st.session_state[f"selected_course_{idx}"] = not st.session_state.get(f"selected_course_{idx}", False)
        
        # Display detailed course information when selected
        for idx, course in enumerate(st.session_state["submitted_courses"]):
            if st.session_state.get(f"selected_course_{idx}", False):
                st.markdown("---")
                
                # Course Header
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.markdown(f"### 🎓 {course['course_name']}")
                with col2:
                    if st.button("❌ Close", key=f"close_{idx}"):
                        st.session_state[f"selected_course_{idx}"] = False
                        st.rerun()
                
                # Course Details
                st.markdown(f"**📝 Description:** {course['course_details']}")
                
                if course['video_file']:
                    st.markdown(f"**🎥 Video File:** {course['video_file']}")
                
                # Modules with expandable sections
                st.markdown("### 📚 Course Modules")
                
                for m_idx, module in enumerate(course['modules']):
                    with st.expander(f"📖 Module {m_idx+1}: {module['name']}", expanded=False):
                        st.markdown(f"**Module Description:** {module.get('description', 'No description available')}")
                        
                        # Topics within module
                        if module['topics']:
                            st.markdown("**🎯 Topics:**")
                            for t_idx, topic in enumerate(module['topics']):
                                with st.expander(f"📝 Topic {t_idx+1}: {topic['name']}", expanded=False):
                                    st.markdown(f"**Topic Description:** {topic.get('description', 'No description available')}")
                                    
                                    # Subtopics within topic
                                    if topic['subtopics']:
                                        st.markdown("**📋 Subtopics:**")
                                        for s_idx, subtopic in enumerate(topic['subtopics']):
                                            if subtopic.strip():  # Only show non-empty subtopics
                                                st.markdown(f"• {subtopic}")
                                    else:
                                        st.info("No subtopics available for this topic.")
                        else:
                            st.info("No topics available for this module.")
                
                st.markdown("---")
    st.stop()

if page == "Add Course":
    st.title("Add a New Course")
    
    # Course input method selection
    input_method = st.radio("Choose input method:", ["Manual Entry", "Fetch from Online"])
    
    if input_method == "Fetch from Online":
        st.subheader("Fetch Course from Online")
        
        # Popular course platforms
        platform = st.selectbox("Select Platform:", [
            "Coursera", "Udemy", "edX", "Pluralsight", "LinkedIn Learning", 
            "Khan Academy", "MIT OpenCourseWare", "Stanford Online", "Custom URL"
        ])
        
        if platform == "Custom URL":
            course_url = st.text_input("Enter Course URL:")
            if course_url:
                if st.button("Fetch Course Details"):
                    try:
                        # Simulate fetching course details (you can integrate with actual APIs)
                        import requests
                        from bs4 import BeautifulSoup
                        
                        headers = {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                        }
                        
                        response = requests.get(course_url, headers=headers, timeout=10)
                        soup = BeautifulSoup(response.content, 'html.parser')
                        
                        # Extract basic course information
                        title = soup.find('title')
                        course_name = title.text.strip() if title else "Online Course"
                        
                        # Extract description
                        description_selectors = [
                            'meta[name="description"]',
                            '.course-description',
                            '.description',
                            '[class*="description"]'
                        ]
                        
                        course_details = ""
                        for selector in description_selectors:
                            desc_elem = soup.select_one(selector)
                            if desc_elem:
                                course_details = desc_elem.get('content') or desc_elem.get_text()
                                break
                        
                        if not course_details:
                            course_details = f"Course fetched from: {course_url}"
                        
                        st.success("Course details fetched successfully!")
                        st.write(f"**Course Name:** {course_name}")
                        st.write(f"**Description:** {course_details[:200]}...")
                        
                        # Pre-fill the form
                        st.session_state.fetched_course_name = course_name
                        st.session_state.fetched_course_details = course_details
                        
                    except Exception as e:
                        st.error(f"Error fetching course details: {str(e)}")
                        st.info("Please try manual entry or check the URL")
        else:
            st.info(f"Selected platform: {platform}")
            st.write("**Popular courses on this platform:**")
            
            # Sample courses for each platform
            sample_courses = {
                "Coursera": [
                    "Machine Learning by Stanford University",
                    "Python for Everybody by University of Michigan",
                    "AWS Fundamentals by Amazon Web Services"
                ],
                "Udemy": [
                    "Complete Python Bootcamp",
                    "AWS Certified Solutions Architect",
                    "Docker and Kubernetes: The Complete Guide"
                ],
                "edX": [
                    "Introduction to Computer Science",
                    "Data Science MicroMasters",
                    "MITx: Introduction to Computer Science"
                ],
                "Pluralsight": [
                    "Python Fundamentals",
                    "AWS Cloud Practitioner",
                    "DevOps Fundamentals"
                ],
                "LinkedIn Learning": [
                    "Python Essential Training",
                    "AWS for Developers",
                    "DevOps Foundations"
                ]
            }
            
            if platform in sample_courses:
                selected_course = st.selectbox("Select a course:", sample_courses[platform])
                if st.button("Use This Course"):
                    st.session_state.fetched_course_name = selected_course
                    st.session_state.fetched_course_details = f"Popular {platform} course: {selected_course}"
                    st.success(f"Selected: {selected_course}")
    
    # Course form (works for both manual and fetched courses)
    st.subheader("Course Details")
    
    # Pre-fill if course was fetched
    default_name = st.session_state.get('fetched_course_name', '')
    default_details = st.session_state.get('fetched_course_details', '')
    
    course_name = st.text_input("Course Name", value=default_name)
    course_details = st.text_area("Course Details", value=default_details)
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
        st.subheader(f"📖 Module {m_idx+1}")
        
        # Module details
        col1, col2 = st.columns([2, 1])
        with col1:
            module["name"] = st.text_input(f"Module Name {m_idx+1}", value=module["name"], key=f"modname{m_idx}")
        with col2:
            module["description"] = st.text_input(f"Module Description {m_idx+1}", value=module.get("description", ""), key=f"moddesc{m_idx}")
        
        num_topics = st.number_input(f"Number of Topics in Module {m_idx+1}", min_value=1, max_value=10, value=len(module["topics"]) or 1, key=f"numtopics{m_idx}")
        
        while len(module["topics"]) < num_topics:
            module["topics"].append({"name": "", "description": "", "subtopics": []})
        while len(module["topics"]) > num_topics:
            module["topics"].pop()
        
        for t_idx, topic in enumerate(module["topics"]):
            st.markdown(f"**📝 Topic {t_idx+1}:**")
            
            # Topic details
            col1, col2 = st.columns([2, 1])
            with col1:
                topic["name"] = st.text_input(f"Topic Name {m_idx+1}-{t_idx+1}", value=topic["name"], key=f"topicname{m_idx}-{t_idx}")
            with col2:
                topic["description"] = st.text_input(f"Topic Description {m_idx+1}-{t_idx+1}", value=topic.get("description", ""), key=f"topicdesc{m_idx}-{t_idx}")
            
            num_subtopics = st.number_input(f"Number of Subtopics in Topic {m_idx+1}-{t_idx+1}", min_value=1, max_value=10, value=len(topic["subtopics"]) or 1, key=f"numsubtopics{m_idx}-{t_idx}")
            
            while len(topic["subtopics"]) < num_subtopics:
                topic["subtopics"].append("")
            while len(topic["subtopics"]) > num_subtopics:
                topic["subtopics"].pop()
            
            for s_idx in range(num_subtopics):
                topic["subtopics"][s_idx] = st.text_input(f"Subtopic Name {m_idx+1}-{t_idx+1}-{s_idx+1}", value=topic["subtopics"][s_idx], key=f"subtopic{m_idx}-{t_idx}-{s_idx}")

    if st.button("Submit Course"):
        if not course_name:
            st.error("Please enter a course name")
        else:
            course_data = {
                "course_name": course_name,
                "course_details": course_details,
                "video_file": video_file.name if video_file else None,
                "modules": st.session_state.modules
            }
            
            # Add to session state for display
            if "submitted_courses" not in st.session_state:
                st.session_state["submitted_courses"] = []
            st.session_state["submitted_courses"].append(course_data)
            
            # Also add to backend database
            try:
                add_course_url = "http://127.0.0.1:8000/add-course"
                backend_data = {
                    "course_name": course_name,
                    "course_details": course_details
                }
                response = requests.post(add_course_url, json=backend_data)
                
                if response.status_code == 200:
                    result = response.json()
                    st.success(f"Course '{course_name}' added successfully!")
                    st.info(f"Course ID: {result.get('course_id')}")
                else:
                    st.warning("Course added to local storage but failed to save to database")
                    st.error(f"Backend error: {response.json().get('error', 'Unknown error')}")
            except Exception as e:
                st.warning("Course added to local storage but failed to save to database")
                st.error(f"Backend connection error: {e}")
            
            st.json(course_data)
            
            # Clear fetched course data
            if 'fetched_course_name' in st.session_state:
                del st.session_state['fetched_course_name']
            if 'fetched_course_details' in st.session_state:
                del st.session_state['fetched_course_details']
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