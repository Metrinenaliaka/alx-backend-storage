-- Create the procedure
CREATE PROCEDURE AddBonus
    @user_id INT,
    @project_name VARCHAR(100),
    @score FLOAT
AS
BEGIN
    -- Check if project_name exists in projects table
    IF NOT EXISTS (SELECT 1 FROM projects WHERE name = @project_name)
    BEGIN
        -- If project_name does not exist, create it
        INSERT INTO projects (name) VALUES (@project_name)
    END

    -- Insert the correction for the student
    INSERT INTO corrections (user_id, project_id, score)
    VALUES (
        @user_id,
        (SELECT id FROM projects WHERE name = @project_name),
        @score
    )
END
