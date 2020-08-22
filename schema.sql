CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT UNIQUE, password TEXT, admin INTEGER DEFAULT 0, teacher INTEGER DEFAULT 0);
CREATE TABLE courses (id SERIAL PRIMARY KEY, name TEXT NOT NULL, teacher_id INTEGER REFERENCES users, course_key TEXT, visible INTEGER DEFAULT 1);
CREATE TABLE exercises (id SERIAL PRIMARY KEY, name TEXT NOT NULL, course_id INTEGER REFERENCES courses, visible INTEGER DEFAULT 1);
CREATE TABLE questions (id SERIAL PRIMARY KEY, question_title TEXT NOT NULL, exercise_id INTEGER REFERENCES exercises, choice_question INTEGER, answer TEXT, points INTEGER, visible INTEGER DEFAULT 1);
CREATE TABLE choices (id SERIAL PRIMARY KEY, choice_title TEXT NOT NULL, question_id INTEGER REFERENCES questions);
CREATE TABLE results (id SERIAL PRIMARY KEY, result INTEGER, max_points INTEGER, exercise_id INTEGER REFERENCES exercises, user_id INTEGER REFERENCES users);
CREATE TABLE answers (id SERIAL PRIMARY KEY, answer TEXT, question_id INTEGER REFERENCES questions, user_id INTEGER REFERENCES users);
CREATE TABLE registrations (id SERIAL PRIMARY KEY, user_id INTEGER REFERENCES users, course_id INTEGER REFERENCES courses);
