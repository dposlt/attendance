CREATE DATABASE dochazka;

CREATE TABLE dochazka (
ID int AUTO_INCREMENT PRIMARY KEY UNIQUE,
name VARCHAR (100) NOT NULL,
prichod TIMESTAMP,
odchod TIMESTAMP
);
