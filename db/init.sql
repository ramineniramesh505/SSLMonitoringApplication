CREATE TABLE IF NOT EXISTS certificates (
    id SERIAL PRIMARY KEY,
    cn VARCHAR(255) NOT NULL,
    expiry DATE NOT NULL,
    notes TEXT
);
