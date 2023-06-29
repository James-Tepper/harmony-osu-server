CREATE TABLE stats (
    user_id INT NOT NULL,
    mode INT NOT NULL,
    action INT NOT NULL,
    info_text TEXT NOT NULL,
    beatmap_md5 TEXT NOT NULL,
    mods INT NOT NULL,
    beatmap_id INT NOT NULL,
    ranked_score INT NOT NULL,
    accuracy DECIMAL NOT NULL,
    play_count INT NOT NULL,
    total_score INT NOT NULL,
    global_rank INT NOT NULL,
    performance_points INT NOT NULL,
    PRIMARY KEY (user_id, mode)
);

CREATE INDEX user_id ON stats (user_id);
CREATE INDEX performance_points ON stats (performance_points);
