-- Setup MySQL database for Lab Attendance System

-- "las" = acronym Lab Attendance System
CREATE DATABASE 'las_db'; 

-- create a user
CREATE USER 'las_db_user'@'localhost' 
IDENTIFIED WITH authentication_plugin 
BY 'Pa$$w0rd123'; -- TODO: CHANGE THE PASSWORD ON THIS LINE !!

GRANT ALL ON las_db.* TO 'las_db_user'@'localhost';