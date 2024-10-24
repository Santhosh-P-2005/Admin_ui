-- create database admin_db;
-- use admin_db;

/* -- Creating table for supersuperadmin
CREATE TABLE supersuperadmin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Creating table for organization
CREATE TABLE organization (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    super_super_admin_id INT,
    FOREIGN KEY (super_super_admin_id) REFERENCES supersuperadmin(id)
);

-- Creating table for superadmin
CREATE TABLE superadmin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    organization_id INT,
    FOREIGN KEY (organization_id) REFERENCES organization(id)
);

-- Creating table for branch
CREATE TABLE branch (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    super_admin_id INT,
    FOREIGN KEY (super_admin_id) REFERENCES superadmin(id)
);

-- Creating table for admin
CREATE TABLE admin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    branch_id INT,
    FOREIGN KEY (branch_id) REFERENCES branch(id)
);

-- Creating table for department
CREATE TABLE department (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    admin_id INT,
    FOREIGN KEY (admin_id) REFERENCES admin(id)
);

-- Creating table for coordinator
CREATE TABLE coordinator (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    department_id INT,
    FOREIGN KEY (department_id) REFERENCES department(id)
);

-- Creating table for member
CREATE TABLE member (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    coordinator_id INT,
    FOREIGN KEY (coordinator_id) REFERENCES coordinator(id)
); */ 
-- show tables
