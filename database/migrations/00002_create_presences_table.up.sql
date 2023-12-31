CREATE TABLE presences (
    presence_id TEXT NOT NULL PRIMARY KEY,
    user_id INT NOT NULL,
    username TEXT NOT NULL,
    action INT NOT NULL,
    rank INT NOT NULL,
    country INT NOT NULL,
    mods INT NOT NULL,
    gamemode INT NOT NULL,
    longitude DECIMAL,
    latitude DECIMAL,
    timezone INT NOT NULL,
    info_text TEXT NOT NULL,
    beatmap_md5 TEXT NOT NULL,
    beatmap_id INT NOT NULL
);
