DELIMITER //

CREATE TRIGGER decrease_quantity_after_order
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    DECLARE item_quantity INT;
    
    -- Get the quantity of the item from the items table
    SELECT quantity INTO item_quantity FROM items WHERE item_id = NEW.item_id;
    
    -- Decrease the quantity by the quantity ordered
    UPDATE items SET quantity = item_quantity - NEW.quantity WHERE item_id = NEW.item_id;
END;
//

DELIMITER ;
