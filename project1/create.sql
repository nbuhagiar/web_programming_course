CREATE TABLE book (
    id SERIAL PRIMARY KEY,
    isbn VARCHAR NOT NULL UNIQUE,
    title VARCHAR NOT NULL,
    author VARCHAR NOT NULL,
    year INTEGER NOT NULL
);

CREATE TABLE member (
    id SERIAL PRIMARY KEY,
    username VARCHAR NOT NULL UNIQUE,
    password VARCHAR NOT NULL
);

CREATE TABLE review (
    id SERIAL PRIMARY KEY,
    username VARCHAR NOT NULL,
    rating INTEGER NOT NULL,
    comment VARCHAR,
    isbn VARCHAR NOT NULL REFERENCES book (isbn),
    UNIQUE (username, isbn)
);