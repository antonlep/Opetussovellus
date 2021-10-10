CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    admin BOOLEAN
);

CREATE TABLE Courses (
    id SERIAL PRIMARY KEY,
    name TEXT,
    visible BOOLEAN
);

CREATE TABLE TextMaterials (
    id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES Courses,
    textmaterial TEXT
);

CREATE TABLE CourseUsers (
    id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES Courses,
    user_id INTEGER REFERENCES Users,
    UNIQUE (course_id, user_id)
);

CREATE TABLE TextQuestions (
    id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES Courses,
    question TEXT,
    answer TEXT,
    visible BOOLEAN
);

CREATE TABLE TextAnswers (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES Users,
    question_id INTEGER REFERENCES TextQuestions,
    answer TEXT,
    time TIMESTAMP
);

CREATE TABLE MultipleChoiceQuestions (
    id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES Courses,
    question TEXT,
    choice1 TEXT,
    choice2 TEXT,
    choice3 TEXT,
    answer INT,
    visible BOOLEAN
);

CREATE TABLE MultipleChoiceAnswers (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES Users,
    question_id INTEGER REFERENCES MultipleChoiceQuestions,
    answer INT,
    time TIMESTAMP
);
