-- Setup MySQL database for Lab Attendance System

-- "las" = acronym Lab Attendance System
DROP DATABASE IF EXISTS las_db;
CREATE DATABASE las_db; 

-- create a user
DROP USER IF EXISTS 'las_db_user'@'localhost';
CREATE USER 'las_db_user'@'localhost'
IDENTIFIED BY 'Pa$$w0rd123'; -- TODO: CHANGE THE PASSWORD ON THIS LINE !!

GRANT ALL PRIVILEGES ON las_db.* TO 'las_db_user'@'localhost';

FLUSH PRIVILEGES;