-- Assuming names table structure: 
-- CREATE TABLE names (
--     id INT PRIMARY KEY,
--     name VARCHAR(100),
--     score INT
-- );

-- Importing the data from names.sql.zip should be done beforehand.

-- Create the index
CREATE INDEX idx_name_first_score ON names (LEFT(name, 1), LEFT(CAST(score AS VARCHAR), 1));
