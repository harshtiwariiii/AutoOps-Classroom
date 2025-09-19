-- Students table
CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY,
    name TEXT
);

-- Student skills table
CREATE TABLE IF NOT EXISTS student_skills (
    student_id INTEGER,
    skill TEXT,
    level REAL,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);
