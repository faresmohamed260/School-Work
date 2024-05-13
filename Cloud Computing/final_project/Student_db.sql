-- Create students table
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    cgpa REAL
);

-- Create account table
CREATE TABLE account (
    account_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    account_type TEXT CHECK(account_type IN ('student', 'admin')),
    student_id INTEGER,
    FOREIGN KEY (student_id) REFERENCES students(id)
);

-- Create subjects table
CREATE TABLE subjects (
    subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    subject_name TEXT,
    grade TEXT CHECK(grade IN ('A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-', 'F')),
    credit_hours INTEGER,
    FOREIGN KEY (student_id) REFERENCES students(id)
);

-- Insert data into the students table
INSERT INTO students (name, age, cgpa) VALUES ('Kareem Ashraf Ahmed', 20, 3.5);
INSERT INTO students (name, age, cgpa) VALUES ('Fares Mohamed Salah', 21, 3.8);

-- Insert data into the accounts table
INSERT INTO account (username, password, account_type, student_id) VALUES ('Km228', '22030171', 'student', 1);
INSERT INTO account (username, password, account_type, student_id) VALUES ('Fares227', '22011614', 'student', 2);

-- Insert data into the subjects table
INSERT INTO subjects (student_id, subject_name, grade, credit_hours) VALUES (1, 'Programming I', 'A-', 3);
INSERT INTO subjects (student_id, subject_name, grade, credit_hours) VALUES (1, 'Programming II', 'B+', 3);
INSERT INTO subjects (student_id, subject_name, grade, credit_hours) VALUES (1, 'Data Minning', 'B', 3);
INSERT INTO subjects (student_id, subject_name, grade, credit_hours) VALUES (2, 'Probability I', 'A', 3);
INSERT INTO subjects (student_id, subject_name, grade, credit_hours) VALUES (2, 'Probability II', 'A-', 3);
INSERT INTO subjects (student_id, subject_name, grade, credit_hours) VALUES (2, 'Linear Algebra', 'B+', 3);

-- SQLite does not support multi-table SELECTs without a common table expression (CTE)
-- Below query selects information from multiple tables and calculates CGPA
-- We need to manually perform this calculation in SQLite
-- You can execute this query separately if you need the result
