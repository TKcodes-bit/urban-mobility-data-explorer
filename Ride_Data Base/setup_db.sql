-- Initialize Database and User for Urban Transport Analytics
CREATE DATABASE IF NOT EXISTS `urban_transport` CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

CREATE USER IF NOT EXISTS 'urban_user'@'%' IDENTIFIED BY 'urban_pass';
GRANT ALL PRIVILEGES ON `urban_transport`.* TO 'urban_user'@'%';

FLUSH PRIVILEGES;
