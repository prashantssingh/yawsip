DROP DATABASE IF EXISTS yawsip;

CREATE DATABASE yawsip;

USE yawsip;

CREATE TABLE user (
    fname VARCHAR(150) NOT NULL,
    lname VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL,
    username VARCHAR(150) NOT NULL PRIMARY KEY,
    password VARCHAR(150) NOT NULL,
    role VARCHAR(30) DEFAULT 'User',
    groupnames VARCHAR(200),
    status VARCHAR(50) DEFAULT 'Pending'
);

CREATE TABLE user_group (
    username VARCHAR(150) NOT NULL,
    groupname VARCHAR(150) NOT NULL
);

CREATE TABLE upload (
    username VARCHAR(150) NOT NULL,
    filename VARCHAR(150) NOT NULL,
    groupname VARCHAR(150) NOT NULL,
    createdat DATETIME DEFAULT CURRENT_TIMESTAMP,
    updatedat DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO user VALUES ("Prashant", "Singh", "94.prashantsingh@gmail.com", "prashantsingh", "helloworld", "Admin", "Approved");
INSERT INTO user VALUES ("Pranit", "Jaiswal", "pranitj@gmail.com", "pranitj", "helloworld", "User", "Group 1, Group 2", "Pending");
INSERT INTO user_group VALUES ("pranitj", "Group 1");
INSERT INTO user_group VALUES ("pranitj", "Group 2");

DROP DATABASE IF EXISTS yawsip;

CREATE DATABASE yawsip;

USE yawsip;

CREATE TABLE user (
    fname VARCHAR(150) NOT NULL,
    lname VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL,
    username VARCHAR(150) NOT NULL PRIMARY KEY,
    password VARCHAR(150) NOT NULL,
    role VARCHAR(30) DEFAULT 'User',
    groupnames VARCHAR(200),
    status VARCHAR(50) DEFAULT 'Pending'
);

CREATE TABLE user_group (
    username VARCHAR(150) NOT NULL,
    groupname VARCHAR(150) NOT NULL
);

CREATE TABLE upload (
    username VARCHAR(150) NOT NULL,
    filename VARCHAR(150) NOT NULL,
    groupname VARCHAR(150) NOT NULL,
    createdat DATETIME DEFAULT CURRENT_TIMESTAMP,
    updatedat DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO user VALUES ("Prashant", "Singh", "94.prashantsingh@gmail.com", "admin", "admin", "Admin", "No Group", "Approved");
INSERT INTO user VALUES ("Pranit", "Jaiswal", "pranitj@gmail.com", "pranitj", "helloworld", "User", "Group 1, Group 2", "Pending");
INSERT INTO user_group VALUES ("pranitj", "Group 1");
INSERT INTO user_group VALUES ("pranitj", "Group 2");

select * from user;

