CREATE DATABASE orbituwa;
CREATE USER IF NOT EXISTS 'orbituwa_admin'@'localhost' IDENTIFIED BY 'orbituwa_admin';
GRANT ALL PRIVILEGES ON `orbituwa`.* TO 'orbituwa_admin'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'admin_orbituwa'@'localhost';
FLUSH PRIVILEGES;