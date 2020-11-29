DROP DATABASE IF EXISTS yawsip;

CREATE DATABASE yawsip;

USE yawsip;

CREATE TABLE user (
    fname VARCHAR(150) NOT NULL,
    lname VARCHAR(150) NOT NULL, 
    username VARCHAR(150) NOT NULL PRIMARY KEY,
    password VARCHAR(150) NOT NULL,
    groupnames VARCHAR(150) NOT NULL,
    status VARCHAR(50) DEFAULT 'Pending'
);

CREATE TABLE usergroup (
    name VARCHAR(150) NOT NULL PRIMARY KEY,
    filename VARCHAR(150) NOT NULL,
    groupname VARCHAR(150) NOT NULL
);