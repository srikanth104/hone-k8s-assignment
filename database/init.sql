CREATE DATABASE IF NOT EXISTS employeesdb;

USE employeesdb;

CREATE TABLE IF NOT EXISTS employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL
);

INSERT INTO employees (name, department) VALUES
('Srikanth', 'Engineering'),
('Aadya', 'Education'),
('John', 'Finance'),
('Mary', 'HR'),
('David', 'Operations'),
('Sarah', 'Engineering'),
('Michael', 'Sales'),
('Priya', 'Marketing'),
('Raj', 'Support'),
('Anita', 'Product');