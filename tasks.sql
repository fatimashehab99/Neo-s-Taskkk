create table users(
	id serial primary key,
	name varchar(50),
	email varchar(50),
	gender varchar(6)
)
create table categories(
	id serial primary key,
	title varchar(20),
	description varchar(100)
)
create table tasks(
	id serial primary key ,
	title varchar(20),
	description varchar(100),
	comleted boolean ,
	sort_number int,
	due_date date,
	user_id int,
	category_id int
)
ALTER TABLE tasks
ADD CONSTRAINT fk_user 
FOREIGN KEY (user_id) REFERENCES users(id);

alter table tasks
add constraint fk_name foreign key
(category_id) references categories(id)

insert into users (name,email,gender) values 
('fatima','fatima@shehab','female'),
('sara','sara@shehb','female')

insert into categories (title,description) values
('work','worrk'),('hobbies','hobbies')