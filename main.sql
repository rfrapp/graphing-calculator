
# Creating a database
CREATE DATABASE test;

# Tells your database engine to use the 
# database named 'test'
USE test;

# Creating a table in the current database
CREATE TABLE scores
(
    id INTEGER NOT NULL AUTO_INCREMENT,
    name VARCHAR(15),
    score INTEGER,
    accuracy INTEGER,
    PRIMARY KEY id
);

# Getting results from a table
SELECT score, name, accuracy FROM scores;
SELECT * FROM scores;
SELECT * FROM scores WHERE id > 6;
SELECT * FROM scores ORDER BY score DESC, accuracy ASC;

# Adding results to a table
INSERT INTO scores (name, score, accuracy) VALUES ('bob', 200, 100);

# Deleting a result or results from a table
DELETE FROM scores WHERE id = 1;
DELETE FROM scores WHERE id > 1;

# Editing a record in a table
UPDATE scores SET name = "joe" WHERE id = 1;
