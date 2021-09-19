CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    admin BOOLEAN
);

CREATE TABLE Courses (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE TextMaterial (
    id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES Courses
);

CREATE TABLE CourseUsers (
    id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES Courses,
    user_id INTEGER REFERENCES Users
);

CREATE TABLE TextQuestions (
    id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES Courses,
    name TEXT,
    content TEXT
);

CREATE TABLE TextAnswers (
    id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES Courses,
    user_id INTEGER REFERENCES Users,
    question_id INTEGER REFERENCES TextQuestions,
    answer TEXT,
    time TIMESTAMP
);

CREATE TABLE MultipleChoiceQuestions (
    id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES Courses,
    question_text TEXT,
    right_answer INTEGER
);

CREATE TABLE MultipleChoiceAnswers (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES Users,
    question_id INTEGER REFERENCES MultipleChoiceQuestions,
    answer INTEGER,
    time TIMESTAMP
);
