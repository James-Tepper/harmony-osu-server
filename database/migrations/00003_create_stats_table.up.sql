CREATE TABLE stats (
    user_id INT NOT NULL,
    play_mode INT NOT NULL,
    action INT NOT NULL,
    status_text TEXT NOT NULL,
    beatmap_checksum TEXT NOT NULL,
    current_mods INT NOT NULL,
    beatmap_id INT NOT NULL,
    ranked_score INT NOT NULL,
    accuracy DECIMAL NOT NULL
    play_count INT NOT NULL,
    total_score INT NOT NULL,
    rank INT NOT NULL,
    performance INT NOT NULL,
    PRIMARY KEY (user_id, play_mode)
);

CREATE INDEX user_id ON stats (user_id);
CREATE INDEX performance ON stats (performance);
