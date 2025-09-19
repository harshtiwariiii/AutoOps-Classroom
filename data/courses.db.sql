-- Courses table
CREATE TABLE IF NOT EXISTS courses (
    course_id INTEGER PRIMARY KEY,
    course_name TEXT
);

-- Course skills table
CREATE TABLE IF NOT EXISTS course_skills (
    course_id INTEGER,
    skill TEXT,
    weight REAL,
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);
