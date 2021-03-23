CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    created TIMESTAMP
);

CREATE TABLE userprofiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    field_key TEXT,
    field_value TEXT
);

CREATE TABLE memes (
    id SERIAL PRIMARY KEY,
    filename TEXT,
    content TEXT,
    user_id INTEGER REFERENCES users,
    visible BOOLEAN DEFAULT TRUE,
    created TIMESTAMP,
    img_data BYTEA
);

CREATE TABLE ratings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    meme_id INTEGER REFERENCES memes,
    points INTEGER DEFAULT 0,
    created TIMESTAMP
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    meme_id INTEGER REFERENCES memes,
    content TEXT NOT NULL,
    visible BOOLEAN DEFAULT TRUE,
    created TIMESTAMP
);

CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    tagword TEXT UNIQUE NOT NULL,
    visible BOOLEAN DEFAULT TRUE,
    created TIMESTAMP
);

CREATE TABLE tagging (
    id SERIAL PRIMARY KEY,
    meme_id INTEGER REFERENCES memes,
    tag_id INTEGER REFERENCES tags
);

