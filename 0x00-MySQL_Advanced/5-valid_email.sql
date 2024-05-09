DELIMITER //
CREATE TRIGGER reset_valid_email
BEFORE UPDATE ON your_table_name
FOR EACH ROW
BEGIN
    IF OLD.email <> NEW.email THEN
        SET NEW.valid_email = 0; -- Reset to invalid when email changes
    END IF;
END;
//
DELIMITER ;
