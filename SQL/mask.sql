-- Create de-identified views of the customers table
CREATE OR REPLACE VIEW deidentified_customers AS
SELECT 
    customer_id,
    CONCAT('Customer_', customer_id) AS anonymized_name,
    CONCAT(SUBSTRING(email, 1, 2), '***@', SUBSTRING_INDEX(email, '@', -1)) AS partial_email,
    YEAR(date_of_birth) AS birth_year,
    QUARTER(date_of_birth) AS birth_quarter,
    YEAR(date_joined) AS join_year,
    MONTH(date_joined) AS join_month
FROM customers;

-- Create de-identified view of the accounts table
CREATE OR REPLACE VIEW deidentified_accounts AS
SELECT 
    account_id,
    account_type,
    CAST(AES_DECRYPT(balance, 'encryption_key') AS DECIMAL(15,2)) / 1000 AS balance_category,
    YEAR(date_opened) AS open_year,
    QUARTER(date_opened) AS open_quarter
FROM accounts;

-- Create de-identified view of the transactions
CREATE OR REPLACE VIEW deidentified_transactions AS
SELECT 
    transaction_id,
    account_id % 1000 AS account_category,
    transaction_type,
    CASE 
        WHEN amount < 500 THEN 'small'
        WHEN amount >= 500 AND amount < 1000 THEN 'medium'
        WHEN amount >= 1000 AND amount < 5000 THEN 'large'
        ELSE 'very_large'
    END AS amount_category,
    YEAR(transaction_date) AS txn_year,
    MONTH(transaction_date) AS txn_month,
    DAYOFWEEK(transaction_date) AS txn_day_of_week,
    CASE
        WHEN transaction_description LIKE '%payroll%' THEN 'income'
        WHEN transaction_description LIKE '%deposit%' THEN 'deposit'
        WHEN transaction_description LIKE '%withdrawal%' THEN 'withdrawal'
        WHEN transaction_description LIKE '%payment%' THEN 'payment'
        WHEN transaction_description LIKE '%transfer%' THEN 'transfer'
        ELSE 'other'
    END AS transaction_category
FROM transactions;

-- Create de-identified employees view
CREATE OR REPLACE VIEW deidentified_employees AS
SELECT
    e_role,
    YEAR(hire_date) AS hire_year,
    TIMESTAMPDIFF(YEAR, hire_date, CURRENT_DATE) AS tenure_years,
    COUNT(*) AS employee_count
FROM employees
GROUP BY e_role, YEAR(hire_date), TIMESTAMPDIFF(YEAR, hire_date, CURRENT_DATE);

-- Create aggregate statistics view for analysis
CREATE OR REPLACE VIEW account_statistics AS
SELECT
    account_type,
    COUNT(*) AS account_count,
    AVG(CAST(AES_DECRYPT(balance, 'encryption_key') AS DECIMAL(15,2))) AS avg_balance,
    MIN(CAST(AES_DECRYPT(balance, 'encryption_key') AS DECIMAL(15,2))) AS min_balance,
    MAX(CAST(AES_DECRYPT(balance, 'encryption_key') AS DECIMAL(15,2))) AS max_balance,
    STDDEV(CAST(AES_DECRYPT(balance, 'encryption_key') AS DECIMAL(15,2))) AS std_dev_balance
FROM accounts
GROUP BY account_type;

-- Create transaction patterns view
CREATE OR REPLACE VIEW transaction_patterns AS
SELECT
    YEAR(t.transaction_date) AS year,
    MONTH(t.transaction_date) AS month,
    a.account_type,
    t.transaction_type,
    COUNT(*) AS transaction_count,
    AVG(t.amount) AS avg_amount,
    SUM(t.amount) AS total_amount
FROM transactions t
JOIN accounts a ON t.account_id = a.account_id
GROUP BY 
    YEAR(t.transaction_date),
    MONTH(t.transaction_date),
    a.account_type,
    t.transaction_type;

-- Create customer segments without PII
CREATE OR REPLACE VIEW customer_segments AS
SELECT
    FLOOR(DATEDIFF(CURRENT_DATE, c.date_of_birth) / 3650) * 10 AS age_decade,
    YEAR(c.date_joined) AS cohort_year,
    COUNT(DISTINCT c.customer_id) AS customer_count,
    COUNT(DISTINCT a.account_id) AS account_count,
    AVG(CAST(AES_DECRYPT(a.balance, 'encryption_key') AS DECIMAL(15,2))) AS avg_balance
FROM customers c
JOIN accounts a ON c.customer_id = a.customer_id
GROUP BY 
    FLOOR(DATEDIFF(CURRENT_DATE, c.date_of_birth) / 3650) * 10,
    YEAR(c.date_joined);

-- Grant access to the de-identified views only
-- REVOKE ALL PRIVILEGES ON bankdb.* FROM 'analyst'@'localhost';
-- GRANT SELECT ON bankdb.deidentified_customers TO 'analyst'@'localhost';
-- GRANT SELECT ON bankdb.deidentified_accounts TO 'analyst'@'localhost';
-- GRANT SELECT ON bankdb.deidentified_transactions TO 'analyst'@'localhost';
-- GRANT SELECT ON bankdb.deidentified_employees TO 'analyst'@'localhost';
-- GRANT SELECT ON bankdb.account_statistics TO 'analyst'@'localhost';
-- GRANT SELECT ON bankdb.transaction_patterns TO 'analyst'@'localhost';
-- GRANT SELECT ON bankdb.customer_segments TO 'analyst'@'localhost';
