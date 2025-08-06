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
    user_id INTEGER REFERENCES users
);


CREATE TABLE characteristics (
    id INTEGER PRIMARY KEY,
    characteristic TEXT
);

CREATE TABLE pet_characteristics (
    pet_id INTEGER REFERENCES pets,
    characteristic_id REFERENCES characteristics
);


CREATE TABLE messages (
    id INTEGER PRIMARY KEY,
    content TEXT,
    sent_at TEXT,
    user_id INTEGER REFERENCES users,
    pet_id INTEGER REFERENCES pets
);

