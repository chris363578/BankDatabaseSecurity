# /Users/bigdata12/projects/BankDatabaseSecurity/bank_project/bank_project/views.py

# Make sure to install the connector: pip install mysql-connector-python
import mysql.connector
from mysql.connector import errorcode

from django.http import HttpResponse
from django.shortcuts import render, redirect # Added render and redirect
from django.views.decorators.csrf import csrf_exempt # Keep for simplicity, consider proper CSRF for production
from pathlib import Path
# Remove: from django.db import connection # We are not using Django's default connection here
import logging # Use logging for better debugging

# Setup logger
logger = logging.getLogger(__name__)

# --- Predefined Queries ---
PREDEFINED_QUERIES = {
    'show_databases': {
        'label': 'SHOW DATABASES;',
        'sql': 'SHOW DATABASES;'
    },
    'show_tables': {
        'label': 'SHOW TABLES FROM bank_db;',
        'sql': 'SHOW TABLES FROM bank_db;' # Make sure db name is correct
    },
    'bank_account_columns': {
        'label': 'SHOW COLUMNS FROM bank_account;',
        'sql': 'SHOW COLUMNS FROM bank_account;'
    },
    'all_accounts_limited': {
        'label': 'SELECT * FROM bank_account LIMIT 10;',
        'sql': 'SELECT * FROM bank_account LIMIT 10;'
    },
    # Add more relevant queries for your users
}

# --- Login View (`about_page`) ---
@csrf_exempt
def login(request):
    """Handles user login, tests connection, and stores credentials in session."""
    error_message = None
    # Pre-fill form values if login fails
    prefill_username = request.POST.get("username", "")
    prefill_instance = request.POST.get("instance", "")

    if request.method == "POST":
        sql_user = request.POST.get("username")
        sql_pass = request.POST.get("password") # NOTE: Storing password in session is insecure!
        sql_instance = request.POST.get("instance")
        db_name = 'bank_db' # Or get from form if needed

        # Basic validation
        if not all([sql_user, sql_pass, sql_instance]):
            error_message = "Username, Password, and Instance IP are required."
            # Re-render form with error
            return render(request, 'login.html', {
                'error_message': error_message,
                'prefill_username': sql_user, # Use submitted values for prefill
                'prefill_instance': sql_instance
            })

        # Construct certificate paths
        try:
            base_dir = Path(__file__).resolve().parent.parent # Project root
            # Adjust this path if your ssl directory is elsewhere relative to views.py
            ssl_base_dir = base_dir / 'bank_project' / 'ssl'
            ssl_user_dir = ssl_base_dir / sql_user

            # Determine if main or replica based on IP
            # NOTE: Ensure this IP matches your actual replica IP if used
            if sql_instance == '34.41.109.178':
                 instance_type = 'replica'
                 cert_subdir = ssl_user_dir / 'replica'
            else:
                 instance_type = 'main'
                 cert_subdir = ssl_user_dir / 'main'

            ssl_ca_path = cert_subdir / 'server-ca.pem'
            ssl_cert_path = cert_subdir / 'client-cert.pem'
            ssl_key_path = cert_subdir / 'client-key.pem'

            logger.info(f"Attempting login for user '{sql_user}' on instance '{sql_instance}' ({instance_type})")
            logger.debug(f"CA Path: {ssl_ca_path} | Exists: {ssl_ca_path.exists()}")
            logger.debug(f"Cert Path: {ssl_cert_path} | Exists: {ssl_cert_path.exists()}")
            logger.debug(f"Key Path: {ssl_key_path} | Exists: {ssl_key_path.exists()}")

            if not all([ssl_ca_path.exists(), ssl_cert_path.exists(), ssl_key_path.exists()]):
                 raise FileNotFoundError("One or more required SSL certificate files not found.")

            # Define connection config for mysql-connector-python
            config = {
                'user': sql_user,
                'password': sql_pass,
                'host': sql_instance,
                'database': db_name,
                'connection_timeout': 10, # seconds
                'ssl_ca': str(ssl_ca_path),
                'ssl_cert': str(ssl_cert_path),
                'ssl_key': str(ssl_key_path),
                'ssl_verify_identity': False # Critical: Disable hostname verification for IP connections
                # 'ssl_verify_cert': True # Default when ssl_ca is provided
            }

            # --- Test Connection ---
            logger.info("Testing database connection...")
            conn_test = mysql.connector.connect(**config)
            logger.info("Connection test successful!")

            # --- Store details in session (handle password securely in production!) ---
            request.session['sql_authenticated'] = True
            request.session['sql_user'] = sql_user
            # WARNING: Storing password in session is insecure. Use IAM or other methods if possible.
            request.session['sql_pass'] = sql_pass
            request.session['sql_instance'] = sql_instance
            request.session['sql_db_name'] = db_name
            request.session['ssl_ca_path'] = str(ssl_ca_path)
            request.session['ssl_cert_path'] = str(ssl_cert_path)
            request.session['ssl_key_path'] = str(ssl_key_path)
            request.session['instance_type'] = instance_type # Store type for display

            conn_test.close() # Close the test connection

            # --- Redirect to dashboard ---
            # Assumes you have a URL pattern named 'sql_dashboard' in urls.py
            return redirect('sql_dashboard')

        except FileNotFoundError as e:
            logger.error(f"Login failed for {sql_user}: {e}")
            error_message = str(e)
        except mysql.connector.Error as err:
            logger.error(f"Login failed for {sql_user}. DB Error: {err}")
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                error_message = "Access Denied: Incorrect username or password."
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                error_message = f"Database '{db_name}' not found or access denied."
            elif "SSL connection error" in err.msg:
                 error_message = f"SSL Connection Error: {err.msg}. Please verify certificates and server SSL configuration."
            else:
                error_message = f"Database Connection Error: ({err.errno}) {err.msg}"
        except Exception as e:
            logger.exception(f"An unexpected error occurred during login for {sql_user}: {e}") # Log full traceback
            error_message = f"An unexpected error occurred: {e}"

        # If any error occurred, re-render the login form with the error
        return render(request, 'login.html', {
            'error_message': error_message,
            'prefill_username': sql_user, # Use submitted values
            'prefill_instance': sql_instance
        })

    # --- Handle GET request (show login form) ---
    # Clear session on fresh login page visit? Optional.
    # request.session.flush()
    return render(request, 'login.html', {
        'prefill_username': prefill_username,
        'prefill_instance': prefill_instance
    })


# --- Dashboard View ---
@csrf_exempt # Keep for simplicity, consider proper CSRF for production
def dashboard(request):
    """Displays predefined queries and results, using connection details from session."""

    # --- Check Authentication ---
    if not request.session.get('sql_authenticated'):
        # Redirect to login if session data is missing
        # Assumes you have a URL pattern named 'login_page' pointing to about_page
        return redirect('login_page') # Or the name of your login URL

    # --- Retrieve Connection Details from Session ---
    sql_user = request.session.get('sql_user')
    sql_pass = request.session.get('sql_pass') # WARNING: Password from session!
    sql_instance = request.session.get('sql_instance')
    sql_db_name = request.session.get('sql_db_name')
    ssl_ca_path = request.session.get('ssl_ca_path')
    ssl_cert_path = request.session.get('ssl_cert_path')
    ssl_key_path = request.session.get('ssl_key_path')
    instance_type = request.session.get('instance_type', 'N/A')

    # Check if all required session data exists
    if not all([sql_user, sql_pass, sql_instance, sql_db_name, ssl_ca_path, ssl_cert_path, ssl_key_path]):
         logger.error("Dashboard access attempt with incomplete session data.")
         # Optionally clear session and redirect
         request.session.flush()
         return redirect('login_page') # Redirect to login

    context = {
        'sql_user': sql_user,
        'sql_instance': sql_instance,
        'instance_type': instance_type,
        'queries': PREDEFINED_QUERIES,
        'selected_query_key': None,
        'query_label': None,
        'headers': [],
        'rows': [],
        'error_message': None,
        'result_message': None,
    }

    # --- Handle Query Execution (POST Request) ---
    if request.method == "POST":
        selected_query_key = request.POST.get('query_key')
        query_info = PREDEFINED_QUERIES.get(selected_query_key)
        context['selected_query_key'] = selected_query_key

        if query_info:
            query = query_info.get('sql')
            context['query_label'] = query_info.get('label')
            logger.info(f"User '{sql_user}' executing query '{context['query_label']}' on instance '{sql_instance}'")

            conn_dash = None # Initialize connection
            try:
                # --- Establish Connection for this query ---
                config = {
                    'user': sql_user,
                    'password': sql_pass, # WARNING: Password from session!
                    'host': sql_instance,
                    'database': sql_db_name,
                    'connection_timeout': 10,
                    'ssl_ca': ssl_ca_path,
                    'ssl_cert': ssl_cert_path,
                    'ssl_key': ssl_key_path,
                    'ssl_verify_identity': False # Critical
                }
                conn_dash = mysql.connector.connect(**config)
                cursor = conn_dash.cursor(dictionary=True) # Use dictionary cursor

                # --- Execute Query ---
                cursor.execute(query)

                # --- Process Results ---
                if cursor.description: # Check if the query produces results (e.g., SELECT)
                    context['headers'] = [col[0] for col in cursor.description]
                    context['rows'] = cursor.fetchall() # Fetch all results
                    if not context['rows']:
                         context['result_message'] = "Query executed successfully, but returned no rows."
                    logger.info(f"Query successful, returned {len(context['rows'])} rows.")
                else: # Handle queries that don't return rows (e.g., SHOW, potentially UPDATE/INSERT if allowed)
                     context['result_message'] = f"Query '{context['query_label']}' executed successfully (no rows returned)."
                     logger.info(f"Query successful, no rows returned (affected rows: {cursor.rowcount}).")


                cursor.close()

            except mysql.connector.Error as err:
                logger.error(f"Dashboard query failed for user '{sql_user}'. DB Error: {err}")
                context['error_message'] = f"Database Error: ({err.errno}) {err.msg}"
                if "SSL connection error" in err.msg:
                    context['error_message'] = f"SSL Connection Error: {err.msg}"
            except Exception as e:
                 logger.exception(f"Unexpected error during dashboard query for {sql_user}: {e}")
                 context['error_message'] = f"An unexpected error occurred: {e}"
            finally:
                if conn_dash and conn_dash.is_connected():
                    conn_dash.close()
                    logger.debug("Dashboard query connection closed.")

        else:
            context['error_message'] = "Invalid query selected."
            logger.warning(f"User '{sql_user}' attempted invalid query key: {selected_query_key}")


    # --- Render Dashboard Page (Handles GET and renders after POST) ---
    return render(request, 'dashboard.html', context)


# --- Logout View (Optional but Recommended) ---
def logout(request):
    """Clears the session and redirects to login."""
    logger.info(f"User '{request.session.get('sql_user', 'Unknown')}' logging out.")
    request.session.flush() # Clears all session data
    return redirect('login_page') # Redirect to login page

