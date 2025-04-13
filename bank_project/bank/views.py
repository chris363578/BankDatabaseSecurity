import pymysql
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from pathlib import Path

@csrf_exempt
def about_page(request):
    if request.method == "POST":
        sql_user = request.POST.get("username")
        sql_pass = request.POST.get("password")
        sql_instance = request.POST.get("instance")
        users = [
            'chris-database-security-project', 
            'customer_user',
            'employee_dbeditor',
            'employee_dbviewer'
        ]

        base_dir = Path(__file__).resolve().parent.parent  # this is project root
        ssl_dir = base_dir / 'bank_project' / 'ssl' / sql_user

        # Set the paths based on the instance
        if sql_instance == '34.41.109.178':
            ssl_cert = ssl_dir / 'replica' / 'client-cert.pem'
            ssl_key = ssl_dir / 'replica' / 'client-key.pem'
            ssl_ca = ssl_dir / 'replica' / 'server-ca.pem'
        else:
            ssl_cert = ssl_dir / 'main' / 'client-cert.pem'
            ssl_key = ssl_dir / 'main' / 'client-key.pem'
            ssl_ca = ssl_dir / 'main' / 'server-ca.pem'

        print("Cert path debug:")
        print("CA     :", ssl_ca, ssl_ca.exists())
        print("Cert   :", ssl_cert, ssl_cert.exists())
        print("Key    :", ssl_key, ssl_key.exists())

        try:
            # Establish SSL connection to MySQL
            conn = pymysql.connect(
                host=sql_instance,
                user=sql_user,
                password=sql_pass,
                database='bank_db',
                ssl={
                    'ca': str(ssl_ca),
                    'cert': str(ssl_cert),
                    'key': str(ssl_key),
                    'check_hostname': True  # Set to True to verify the certificate
                }
            )
            
            with conn.cursor() as cursor:
                cursor.execute("SELECT CURRENT_USER();")
                user_info = cursor.fetchone()

            return HttpResponse(f"<h1>SSL Login successful as {user_info[0]}</h1>")

        except Exception as e:
            return HttpResponse(f"<h1>Connection failed</h1><pre>{str(e)}</pre>")

    return HttpResponse("""
    <html>
    <head><title>SQL SSL Login</title></head>
    <body>
        <h2>Login to Cloud SQL</h2>
        <form method="POST">
            <input type="text" name="username" placeholder="SQL Username"><br><br>
            <input type="password" name="password" placeholder="SQL Password"><br><br>
            <input type="text" name="instance" placeholder="Instance IP or Hostname"><br><br>
            <button type="submit">Login</button>
        </form>
    </body>
    </html>
    """)

from django.http import HttpResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

PREDEFINED_QUERIES = {
    'bank_account_columns': {
        'label': 'SHOW COLUMNS FROM bank_account;',
        'sql': 'SHOW COLUMNS FROM bank_account;'
    },
    'all_accounts': {
        'label': 'SELECT * FROM bank_account LIMIT 10;',
        'sql': 'SELECT * FROM bank_account LIMIT 10;'
    },
    # Add more queries here
}

@csrf_exempt
def sql_dashboard(request):
    result_html = ""
    selected_query_key = None

    if request.method == "POST":
        selected_query_key = request.POST.get('query_key')
        query = PREDEFINED_QUERIES.get(selected_query_key, {}).get('sql')

        if query:
            with connection.cursor() as cursor:
                cursor.execute(query)
                headers = [col[0] for col in cursor.description] if cursor.description else []
                rows = cursor.fetchall()

                # Build HTML table
                result_html += "<table border='1'><thead><tr>"
                result_html += "".join(f"<th>{header}</th>" for header in headers)
                result_html += "</tr></thead><tbody>"
                for row in rows:
                    result_html += "<tr>" + "".join(f"<td>{col}</td>" for col in row) + "</tr>"
                result_html += "</tbody></table>"

    # Build buttons for predefined queries
    buttons_html = ""
    for key, info in PREDEFINED_QUERIES.items():
        buttons_html += f"""
        <form method="POST" style="display:inline;">
            <input type="hidden" name="query_key" value="{key}">
            <button type="submit">{info['label']}</button>
        </form>
        """

    # Final page
    html = f"""
    <html>
    <head>
        <title>SQL Dashboard</title>
    </head>
    <body>
        <h1>Predefined SQL Dashboard</h1>
        {buttons_html}
        <hr>
        {f"<h3>Result for: {PREDEFINED_QUERIES[selected_query_key]['label']}</h3>" if selected_query_key else ""}
        {result_html}
    </body>
    </html>
    """

    return HttpResponse(html)
