# Running MySQL Files

This guide explains how to execute MySQL files (.sql) using different methods, including the MySQL command line, MySQL Workbench, and via a script.

## Prerequisites
- MySQL Server installed on your system.
- MySQL Client or MySQL Workbench.
- A database user with necessary permissions.

## Running MySQL Files via Command Line

### 1. Open the MySQL Command Line
- On Windows: Open Command Prompt (`cmd`) or PowerShell.
- On macOS/Linux: Open Terminal.

### 2. Connect to MySQL Server
```sh
mysql -u your_username -p
```
- Replace `your_username` with your MySQL username.
- Enter your password when prompted.

### 3. Select the Target Database (If Required)
```sql
USE database_name;
```
- Replace `database_name` with the name of your database.

### 4. Execute the SQL File
```sh
SOURCE /path/to/your/file.sql;
```
- Replace `/path/to/your/file.sql` with the actual path of your `.sql` file.

## Running MySQL Files in MySQL Workbench

1. Open **MySQL Workbench**.
2. Connect to your database instance.
3. Click on **File > Open SQL Script**.
4. Select your `.sql` file.
5. Click on **Execute (⚡ Run)** to run the script.

## Running MySQL Files in a Script (Python Example)
If you want to execute an SQL file within a Python script, you can use the `mysql-connector-python` library:

```python
import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    database="your_database"
)

cursor = conn.cursor()

# Read SQL file
with open("file.sql", "r") as file:
    sql_script = file.read()

# Execute SQL commands
for statement in sql_script.split(';'):
    if statement.strip():
        cursor.execute(statement)

# Commit changes and close connection
conn.commit()
cursor.close()
conn.close()
```

## Troubleshooting
- **"Access denied" error**: Ensure the user has the correct permissions.
- **File not found**: Double-check the file path and ensure it exists.
- **Syntax errors**: Validate the SQL syntax in the file before execution.

For more details, refer to the [MySQL Documentation](https://dev.mysql.com/doc/).

