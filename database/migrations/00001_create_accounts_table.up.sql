CREATE TABLE accounts (
    user_id SERIAL NOT NULL,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

