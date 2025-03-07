-- Populating customers table
INSERT INTO customers (customer_id, customer_name, email, phone_number, address, date_of_birth, date_joined, ssn) VALUES
(1001, 'John Smith', 'john.smith@email.com', AES_ENCRYPT('555-123-4567', 'encryption_key'), AES_ENCRYPT('123 Main St, Springfield, IL 62701', 'encryption_key'), '1985-06-15', '2018-02-10 09:30:00', AES_ENCRYPT('123-45-6789', 'encryption_key')),
(1002, 'Sarah Johnson', 'sarah.j@email.com', AES_ENCRYPT('555-234-5678', 'encryption_key'), AES_ENCRYPT('456 Oak Ave, Springfield, IL 62702', 'encryption_key'), '1990-08-22', '2019-04-15 10:45:00', AES_ENCRYPT('234-56-7890', 'encryption_key')),
(1003, 'Michael Brown', 'mbrown@email.com', AES_ENCRYPT('555-345-6789', 'encryption_key'), AES_ENCRYPT('789 Pine Rd, Springfield, IL 62703', 'encryption_key'), '1978-11-30', '2017-07-22 14:15:00', AES_ENCRYPT('345-67-8901', 'encryption_key')),
(1004, 'Jennifer Davis', 'jdavis@email.com', AES_ENCRYPT('555-456-7890', 'encryption_key'), AES_ENCRYPT('101 Maple Dr, Springfield, IL 62704', 'encryption_key'), '1982-03-18', '2020-01-05 11:20:00', AES_ENCRYPT('456-78-9012', 'encryption_key')),
(1005, 'Robert Wilson', 'rwilson@email.com', AES_ENCRYPT('555-567-8901', 'encryption_key'), AES_ENCRYPT('202 Elm St, Springfield, IL 62705', 'encryption_key'), '1975-09-05', '2016-11-12 13:10:00', AES_ENCRYPT('567-89-0123', 'encryption_key')),
(1006, 'Lisa Martinez', 'lmartinez@email.com', AES_ENCRYPT('555-678-9012', 'encryption_key'), AES_ENCRYPT('303 Cedar Ln, Springfield, IL 62706', 'encryption_key'), '1992-12-10', '2021-03-08 09:05:00', AES_ENCRYPT('678-90-1234', 'encryption_key')),
(1007, 'David Thompson', 'dthompson@email.com', AES_ENCRYPT('555-789-0123', 'encryption_key'), AES_ENCRYPT('404 Birch Blvd, Springfield, IL 62707', 'encryption_key'), '1980-05-25', '2018-08-30 15:45:00', AES_ENCRYPT('789-01-2345', 'encryption_key')),
(1008, 'Emily Anderson', 'eanderson@email.com', AES_ENCRYPT('555-890-1234', 'encryption_key'), AES_ENCRYPT('505 Walnut Ave, Springfield, IL 62708', 'encryption_key'), '1988-07-14', '2019-10-18 12:30:00', AES_ENCRYPT('890-12-3456', 'encryption_key')),
(1009, 'James Taylor', 'jtaylor@email.com', AES_ENCRYPT('555-901-2345', 'encryption_key'), AES_ENCRYPT('606 Spruce St, Springfield, IL 62709', 'encryption_key'), '1973-01-29', '2017-05-02 10:00:00', AES_ENCRYPT('901-23-4567', 'encryption_key')),
(1010, 'Amanda Garcia', 'agarcia@email.com', AES_ENCRYPT('555-012-3456', 'encryption_key'), AES_ENCRYPT('707 Aspen Ct, Springfield, IL 62710', 'encryption_key'), '1995-04-03', '2022-02-25 14:20:00', AES_ENCRYPT('012-34-5678', 'encryption_key'));

-- Populating accounts table
INSERT INTO accounts (account_id, customer_id, account_type, balance, date_opened) VALUES
(5001, 1001, 'checking', AES_ENCRYPT('5250.75', 'encryption_key'), '2018-02-10 10:15:00'),
(5002, 1001, 'savings', AES_ENCRYPT('15780.50', 'encryption_key'), '2018-02-10 10:30:00'),
(5003, 1002, 'checking', AES_ENCRYPT('3200.25', 'encryption_key'), '2019-04-15 11:00:00'),
(5004, 1002, 'savings', AES_ENCRYPT('8500.00', 'encryption_key'), '2019-04-15 11:15:00'),
(5005, 1003, 'business', AES_ENCRYPT('42500.60', 'encryption_key'), '2017-07-22 14:30:00'),
(5006, 1004, 'checking', AES_ENCRYPT('1850.30', 'encryption_key'), '2020-01-05 11:45:00'),
(5007, 1004, 'savings', AES_ENCRYPT('6700.00', 'encryption_key'), '2020-01-05 12:00:00'),
(5008, 1005, 'checking', AES_ENCRYPT('9250.00', 'encryption_key'), '2016-11-12 13:30:00'),
(5009, 1006, 'savings', AES_ENCRYPT('12500.75', 'encryption_key'), '2021-03-08 09:20:00'),
(5010, 1007, 'checking', AES_ENCRYPT('4350.25', 'encryption_key'), '2018-08-30 16:00:00'),
(5011, 1007, 'savings', AES_ENCRYPT('22780.90', 'encryption_key'), '2018-08-30 16:15:00'),
(5012, 1008, 'checking', AES_ENCRYPT('2900.50', 'encryption_key'), '2019-10-18 12:45:00'),
(5013, 1009, 'business', AES_ENCRYPT('68350.25', 'encryption_key'), '2017-05-02 10:30:00'),
(5014, 1010, 'checking', AES_ENCRYPT('1650.30', 'encryption_key'), '2022-02-25 14:35:00'),
(5015, 1010, 'savings', AES_ENCRYPT('5800.00', 'encryption_key'), '2022-02-25 14:50:00');

-- Populating transactions table
INSERT INTO transactions (transaction_id, account_id, transaction_type, amount, transaction_date, transaction_description) VALUES
(10001, 5001, 'deposit', 1500.00, '2023-01-05 09:30:00', 'Payroll deposit'),
(10002, 5001, 'withdrawl', 200.00, '2023-01-10 14:15:00', 'ATM withdrawal'),
(10003, 5002, 'deposit', 2500.00, '2023-01-12 11:20:00', 'Transfer from checking'),
(10004, 5003, 'payment', 450.75, '2023-01-15 13:45:00', 'Utility bill payment'),
(10005, 5003, 'deposit', 2200.00, '2023-01-18 10:05:00', 'Payroll deposit'),
(10006, 5004, 'transfer', 1000.00, '2023-01-20 15:30:00', 'Transfer to checking'),
(10007, 5005, 'deposit', 8500.50, '2023-01-22 09:15:00', 'Business revenue'),
(10008, 5005, 'payment', 3250.75, '2023-01-25 14:20:00', 'Vendor payment'),
(10009, 5006, 'deposit', 1450.00, '2023-01-28 10:30:00', 'Payroll deposit'),
(10010, 5007, 'transfer', 500.00, '2023-01-30 12:45:00', 'Automatic transfer from checking'),
(10011, 5008, 'withdrawl', 1000.00, '2023-02-02 11:10:00', 'ATM withdrawal'),
(10012, 5009, 'deposit', 1500.00, '2023-02-05 09:45:00', 'Mobile check deposit'),
(10013, 5010, 'payment', 750.25, '2023-02-08 13:20:00', 'Mortgage payment'),
(10014, 5011, 'transfer', 1200.00, '2023-02-10 15:50:00', 'Transfer to checking'),
(10015, 5012, 'deposit', 1850.00, '2023-02-12 10:15:00', 'Payroll deposit'),
(10016, 5013, 'payment', 5430.50, '2023-02-15 14:30:00', 'Supplier payment'),
(10017, 5014, 'withdrawl', 300.00, '2023-02-18 12:25:00', 'ATM withdrawal'),
(10018, 5015, 'deposit', 1000.00, '2023-02-20 09:10:00', 'Transfer from checking'),
(10019, 5001, 'payment', 125.50, '2023-02-22 11:40:00', 'Phone bill payment'),
(10020, 5003, 'deposit', 1600.00, '2023-02-25 10:35:00', 'Check deposit');

-- Populating employees table
INSERT INTO employees (employee_id, first_name, last_name, email, phone, hire_date, e_role) VALUES
(101, 'Thomas', 'Miller', 'tmiller@bank.com', '555-111-2222', '2015-06-10', 'manager'),
(102, 'Jessica', 'Lee', 'jlee@bank.com', '555-222-3333', '2017-03-15', 'banker'),
(103, 'Daniel', 'Clark', 'dclark@bank.com', '555-333-4444', '2018-09-22', 'advisor'),
(104, 'Rebecca', 'Wright', 'rwright@bank.com', '555-444-5555', '2019-11-05', 'banker'),
(105, 'Mark', 'Johnson', 'mjohnson@bank.com', '555-555-6666', '2016-08-18', 'advisor'),
(106, 'Laura', 'Walker', 'lwalker@bank.com', '555-666-7777', '2020-01-20', 'reception'),
(107, 'Christopher', 'Harris', 'charris@bank.com', '555-777-8888', '2017-05-12', 'banker'),
(108, 'Michelle', 'Martin', 'mmartin@bank.com', '555-888-9999', '2021-04-02', 'reception'),
(109, 'Kevin', 'Thompson', 'kthompson@bank.com', '555-999-0000', '2018-12-15', 'advisor'),
(110, 'Elizabeth', 'White', 'ewhite@bank.com', '555-000-1111', '2019-07-08', 'manager');
