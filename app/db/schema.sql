-- POSTGRES schema for the server

CREATE TABLE users (
    email VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    discord_user VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE pairings (
    id SERIAL PRIMARY KEY,
    user1_email VARCHAR(255) REFERENCES users(email) NOT NULL,
    user2_email VARCHAR(255) REFERENCES users(email) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    question_url VARCHAR(255) NOT NULL,
    question_number INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE forms (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email_response_id VARCHAR(255) NOT NULL,
    discord_response_id VARCHAR(255) NOT NULL,
    name_response_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE form_responses (
    id SERIAL PRIMARY KEY,
    form_id INT REFERENCES forms(id) NOT NULL,
    user_email VARCHAR(255) REFERENCES users(email) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE email_records (
    id SERIAL PRIMARY KEY,
    user_email VARCHAR(255) REFERENCES users(email) NOT NULL,
    email_contents TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);