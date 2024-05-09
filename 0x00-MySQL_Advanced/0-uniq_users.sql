-- Check if the table exists before creating it
IF NOT EXISTS (SELECT * FROM information_schema.tables WHERE table_name = 'users') THEN
    -- Create the table users if it does not exist
    CREATE TABLE users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(255) NOT NULL UNIQUE,
        name VARCHAR(255)
    );
END IF;
