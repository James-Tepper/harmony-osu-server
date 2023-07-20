CREATE TABLE scores (
    user_id INT NOT NULL,
    performance_points INT,
    accuracy DECIMAL NOT NULL,
    ranked_score INT NOT NULL,
    mods INT NOT NULL,
    mode INT NOT NULL,
    beatmap_id INT NOT NULL
);

CREATE INDEX score_user_id ON scores (user_id);

-- performance points can be NULL for unranked/loved maps
