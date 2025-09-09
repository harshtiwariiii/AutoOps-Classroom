import sqlite3

# Create students.db and courses.db
students_conn = sqlite3.connect('data/students.db')
courses_conn = sqlite3.connect('data/courses.db')

# Create tables for students.db
students_conn.executescript('''
CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY,
    name TEXT
);
CREATE TABLE IF NOT EXISTS student_skills (
    student_id INTEGER,
    skill TEXT,
    level REAL,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);
''')

# Create tables for courses.db
courses_conn.executescript('''
CREATE TABLE IF NOT EXISTS courses (
    course_id INTEGER PRIMARY KEY,
    course_name TEXT
);
CREATE TABLE IF NOT EXISTS course_skills (
    course_id INTEGER,
    skill TEXT,
    weight REAL,
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);
''')

# Insert sample data into students.db
students_conn.execute("INSERT INTO students (student_id, name) VALUES (1, 'Alice')")
students_conn.execute("INSERT INTO students (student_id, name) VALUES (2, 'Bob')")
students_conn.executemany(
    "INSERT INTO student_skills (student_id, skill, level) VALUES (?, ?, ?)",
    [
        (1, 'python', 3),
        (1, 'cli', 1),
        (1, 'networking', 2),
        (2, 'python', 5),
        (2, 'aws', 2)
    ]
)

# Insert sample data into courses.db
courses_conn.execute("INSERT INTO courses (course_id, course_name) VALUES (1, 'AWS Basics')")
courses_conn.execute("INSERT INTO courses (course_id, course_name) VALUES (2, 'Python Boot')")
courses_conn.executemany(
    "INSERT INTO course_skills (course_id, skill, weight) VALUES (?, ?, ?)",
    [
        (1, 'python', 1),
        (1, 'cli', 4),
        (1, 'networking', 9),
        (2, 'python', 10),
        (2, 'cli', 1)
    ]
)

students_conn.commit()
courses_conn.commit()
students_conn.close()
courses_conn.close()

print('Databases and sample data created successfully.')
