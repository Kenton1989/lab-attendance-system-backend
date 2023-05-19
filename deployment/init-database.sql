-- Setup MySQL database for Lab Attendance System

-- "las" = acronym Lab Attendance System
DROP DATABASE IF EXISTS las_db;
CREATE DATABASE las_db; 

-- create a user
CREATE USER 'las-db-user'@'localhost' IDENTIFIED 
BY 'Pa$$w0rd123'; -- TODO: CHANGE THE PASSWORD ON THIS LINE !!

GRANT ALL PRIVILEGES ON las_db.* TO 'las-db-user'@'localhost';

FLUSH PRIVILEGES;