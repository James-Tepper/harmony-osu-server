CREATE TABLE presences (
    presence_id TEXT NOT NULL PRIMARY KEY,
    user_id INT NOT NULL,
    username TEXT NOT NULL,
    timezone INT NOT NULL,
    country INT NOT NULL,
    permission INT NOT NULL,
    longitude DECIMAL,
    latitude DECIMAL,
    rank INT NOT NULL,
    gamemode INT NOT NULL
);
