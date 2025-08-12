CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT,
    image BLOB
);

CREATE TABLE pets (
    id INTEGER PRIMARY KEY,
    name TEXT,
    species TEXT,
    breed TEXT,
    image BLOB,
    user_id INTEGER REFERENCES users,
    activity_id INTEGER REFERENCES activity,
    appetite_id INTEGER REFERENCES appetite
);


CREATE TABLE activity (
    id INTEGER PRIMARY KEY,
    activity TEXT
);

INSERT INTO activity (activity) VALUES 
('erittäin vilkas'), 
('vilkas'), 
('tavallinen'), 
('laiska'), 
('erittäin laiska')
;

CREATE TABLE appetite (
    id INTEGER PRIMARY KEY,
    appetite TEXT
);

INSERT INTO appetite (appetite) VALUES 
('erittäin ahne'),
('ahne'),
('tavallinen'),
('nirso'),
('erittäin nirso')
;


CREATE TABLE messages (
    id INTEGER PRIMARY KEY,
    content TEXT,
    sent_at TEXT,
    user_id INTEGER REFERENCES users,
    pet_id INTEGER REFERENCES pets
);

