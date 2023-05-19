-- Setup MySQL database for Lab Attendance System

-- "las" = acronym Lab Attendance System
CREATE DATABASE 'las_db'; 

-- !!! substitute the Pa$$w0rd123 below with proper password !!!
CREATE USER 'las_db_user'@'localhost' IDENTIFIED WITH authentication_plugin BY 'Pa$$w0rd123'; 

GRANT ALL ON las_db.* TO 'las_db_user'@'localhost';