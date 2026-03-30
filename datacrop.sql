CREATE DATABASE cropdoctor;

USE cropdoctor;

CREATE TABLE predictions (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    image_name    VARCHAR(255),
    disease_name  VARCHAR(255),
    confidence    FLOAT,
    description   TEXT,
    symptoms      TEXT,
    remedies      TEXT,
    predicted_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

SELECT * FROM predictions