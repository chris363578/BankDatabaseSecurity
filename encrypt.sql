set @aes_key = 'thisisthekey';

describe customers;

alter table customers modify column customer_id int not null default 0;
alter table customers modify column customer_name varchar(100) default 'name';
alter table customers modify column email varchar(255) not null default 'email';


insert into customers(customer_id, customer_name, email) values(12347, 'jerry smith', 'jerryemail@gmail.com');

update customers
set ssn = aes_encrypt('111-222-3333', @aes_key)
where customer_id = 12346;


select ssn 
from customers
where customer_id = 12346;

SELECT customer_id, CAST(AES_DECRYPT(ssn, @aes_key) AS CHAR) AS decrypted_ssn
FROM customers
WHERE customer_id = 12346;

select HEX(ssn) from customers;