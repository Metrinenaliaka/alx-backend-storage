DELIMITER //

CREATE PROCEDURE ComputeAverageScoreForUser (
    IN user_id INT
)
BEGIN
    DECLARE avg_score DECIMAL(10, 2);
    
    -- Calculate average score
    SELECT AVG(score) INTO avg_score
    FROM scores
    WHERE user_id = user_id;
    
    -- Insert or update average score in user_scores table
    IF EXISTS (SELECT 1 FROM user_scores WHERE user_id = user_id) THEN
        UPDATE user_scores
        SET average_score = avg_score
        WHERE user_id = user_id;
    ELSE
        INSERT INTO user_scores (user_id, average_score)
        VALUES (user_id, avg_score);
    END IF;
END //

DELIMITER ;
