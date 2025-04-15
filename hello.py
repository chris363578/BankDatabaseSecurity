import mysql.connector
from mysql.connector import errorcode
from pathlib import Path
import getpass
import ssl # To print OpenSSL version

# --- Connection Parameters ---
# !! Replace with your actual database name if different !!
db_name = 'bank_db'
# The user we are testing with
sql_user = 'employee_dbviewer'
# The IP address of the Cloud SQL instance
sql_instance_ip = '104.155.140.227'

# --- Certificate Paths ---
# !! IMPORTANT: Verify this base path is correct for your project structure !!
# Using absolute path based on previous logs
base_cert_dir = Path('/Users/bigdata12/projects/BankDatabaseSecurity/bank_project/bank_project/ssl')

# Construct paths for the specific user and instance type ('main')
user_cert_dir = base_cert_dir / sql_user / 'main'
ssl_ca_path = user_cert_dir / 'server-ca.pem'
ssl_cert_path = user_cert_dir / 'client-cert.pem'
ssl_key_path = user_cert_dir / 'client-key.pem'

# --- Main Connection Logic ---
if __name__ == "__main__":
    print("--- Cloud SQL MySQL Connector/Python Connection Test ---")
    # Note: mysql-connector might use system SSL differently, version may not reflect pymysql's context
    print(f"Python SSL Version (for context): {ssl.OPENSSL_VERSION}")
    print(f"MySQL Connector Version: {mysql.connector.__version__}")
    print("-" * 40)
    print(f"Target Instance IP: {sql_instance_ip}")
    print(f"Target User: {sql_user}")
    print(f"Target DB: {db_name}")
    print("-" * 40)
    print("Certificate Paths:")
    print(f"  CA Cert : {ssl_ca_path} | Exists: {ssl_ca_path.exists()}")
    print(f"  Client Cert: {ssl_cert_path} | Exists: {ssl_cert_path.exists()}")
    print(f"  Client Key : {ssl_key_path} | Exists: {ssl_key_path.exists()}")
    print("-" * 40)

    # Check if certificate files exist before proceeding
    if not all([ssl_ca_path.exists(), ssl_cert_path.exists(), ssl_key_path.exists()]):
        print("ERROR: One or more certificate files not found at the specified paths.")
        exit(1)

    # Get password securely
    try:
        sql_pass = getpass.getpass(f"Enter password for user '{sql_user}': ")
    except Exception as e:
        print(f"Error getting password: {e}")
        exit(1)

    # Define connection arguments for mysql-connector-python
    # Note: It uses individual ssl_* arguments, not a dict
    # Hostname verification is typically off by default when ssl_verify_cert is False or CA is provided,
    # but we explicitly disable it via ssl_verify_identity=False.
    config = {
        'user': sql_user,
        'password': sql_pass,
        'host': sql_instance_ip,
        'database': db_name,
        'connection_timeout': 10,
        'ssl_ca': str(ssl_ca_path),
        'ssl_cert': str(ssl_cert_path),
        'ssl_key': str(ssl_key_path),
        'ssl_verify_identity': False # Explicitly disable hostname verification
        # 'ssl_verify_cert': True # Use CA to verify server cert (default True when ssl_ca is provided)
    }
    print(f"Connector Config Used (excluding password):")
    for k, v in config.items():
        if k != 'password':
            print(f"  {k}: {v}")
    print("-" * 40)


    conn = None  # Initialize connection variable
    try:
        print("Attempting to connect using mysql.connector...")
        conn = mysql.connector.connect(**config)
        print("\n✅ SUCCESS: Connection established successfully!")

        # Optional: Run a simple query to verify
        cursor = conn.cursor(dictionary=True) # Get results as dicts
        print("\nRunning test query: SELECT @@hostname, CURRENT_USER();")
        cursor.execute("SELECT @@hostname as server_hostname, CURRENT_USER() as connected_user;")
        result = cursor.fetchone()
        print("\nQuery Result:")
        if result:
            print(f"  Server Hostname: {result.get('server_hostname', 'N/A')}")
            print(f"  Connected as User: {result.get('connected_user', 'N/A')}")
        else:
            print("  Query returned no results.")
        cursor.close()

    except mysql.connector.Error as err:
        print(f"\n❌ FAILURE: Failed to connect using mysql.connector.")
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("  Error: Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print(f"  Error: Database '{db_name}' does not exist")
        else:
            print(f"  Error Number: {err.errno}")
            print(f"  Error Message: {err.msg}")
            # Check for SSL specific details within the error message
            if "SSL connection error" in err.msg:
                 print(f"  SSL Specific Error: {err.msg}")

    except Exception as e:
        print(f"\n❌ FAILURE: An unexpected error occurred.")
        print(f"Error Type: {type(e)}")
        print(f"Error Details: {e}")

    finally:
        if conn and conn.is_connected():
            conn.close()
            print("\nConnection closed.")
        print("\n--- Test Complete ---")
