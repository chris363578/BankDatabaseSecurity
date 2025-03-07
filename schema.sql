show databases;

use bankdb;
show tables;

create table if not exists customers (
	customer_id int primary key not null,
    customer_name varchar(100) not null,
    email varchar(255) not null,
    phone_number varchar(15),
    address varchar(100),
    date_of_birth date,
    date_joined timestamp
);

create table if not exists accounts (
	account_id int primary key not null,
	customer_id int,
	account_type ENUM('checking', 'savings', 'business') NOT NULL,
	balance decimal(15,2) not null,
	date_opened timestamp,
	foreign key (customer_id) references customers(customer_id)
);

create table if not exists transactions (
	transaction_id int primary key not null,
    account_id int,
    transaction_type ENUM('deposit', 'withdrawl', 'transfer', 'payment') not null,
    amount decimal(15, 2) not null,
    transaction_date timestamp,
    transaction_description text
);

alter table transactions
add foreign key(account_id) references accounts(account_id);

create table if not exists employees (
	employee_id int primary key not null,
    first_name varchar(100) not null,
    last_name varchar(100) not null,
    email varchar(100) not null,
    phone varchar(15),
    hire_date date not null,
    e_role ENUM('banker', 'advisor', 'manager', 'reception')
);

alter table customers add column ssn varbinary(255);
alter table customers modify column phone_number varbinary(255);
alter table customers modify column address varbinary(255);

alter table accounts modify column balance varbinary(255);

describe customers;




