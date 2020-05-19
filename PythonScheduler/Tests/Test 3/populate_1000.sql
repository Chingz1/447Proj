CREATE SCHEMA IF NOT EXISTS umbc;

CREATE TABLE IF NOT EXISTS `umbc`.`Schedule` (
  `Subject` VARCHAR(45) NOT NULL,
  `Course #` VARCHAR(45) NOT NULL,
  `Course Title` VARCHAR(45) NULL DEFAULT NULL,
  `Version` INT(11) NULL DEFAULT NULL,
  `Section` INT(11) NOT NULL,
  `Instructor Real Name` VARCHAR(45) NULL DEFAULT NULL,
  `Time` VARCHAR(45) NULL DEFAULT NULL,
  `Capacity` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`Subject`, `Course #`, `Section`));
  
drop procedure if exists doWhile;
DELIMITER //  
CREATE PROCEDURE doWhile()   
BEGIN
DECLARE i INT DEFAULT 1; 
WHILE (i <= 1000) DO
    INSERT INTO `schedule` values ('CMSC', i, 'Computer Science', 1, 1, 'Staff', 'tt530', 50);
    SET i = i+1;
END WHILE;
END;
//  

CALL doWhile();


Select * from Schedule;
