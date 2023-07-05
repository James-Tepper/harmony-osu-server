CREATE TABLE channels (
    name TEXT NOT NULL,
    topic TEXT NOT NULL,
    read_privileges INT NOT NULL,
    write_privileges INT NOT NULL,
    auto_join BOOLEAN NOT NULL,
    temporary BOOLEAN NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
)

CREATE INDEX name ON channels (name)
