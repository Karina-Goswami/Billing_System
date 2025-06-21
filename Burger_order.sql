use project;

create table Burger_orders(
order_id int primary key auto_increment,
item_name varchar(50),
price decimal(10,2),
quantity int,
total decimal(10,2),
student_discount boolean,
delivery boolean,
tip int,
final_total decimal(10,2),
order_time timestamp default current_timestamp
);

select * from Burger_orders;


DESC Burger_orders;





