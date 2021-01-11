DROP DATABASE IF EXISTS yawsip;

CREATE DATABASE yawsip;

USE yawsip;

CREATE TABLE user (
    fname VARCHAR(150) NOT NULL,
    lname VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL,
    username VARCHAR(150) NOT NULL PRIMARY KEY,
    password VARCHAR(500) NOT NULL,
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
    createdate DATETIME DEFAULT CURRENT_TIMESTAMP,
    updatedate DATETIME DEFAULT CURRENT_TIMESTAMP
);
