create database project;

use project;

create table Burger_menu(
Sr int primary key AUTO_INCREMENT,
name varchar(100),
price int);

insert into Burger_menu(name,price) values
("aloo tikki",5),
("maharaja",10),
("mac special",15);

select * from Burger_menu;

