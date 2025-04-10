from django.shortcuts import render
from django.http import HttpResponse
import pymysql
from django.views.decorators.csrf import csrf_exempt
from pathlib import Path
from google.cloud import logging_v2
from django.http import JsonResponse

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

        #sql_user = users[3]
        #sql_pass = 'password'


        base_dir = Path(__file__).resolve().parent.parent  # this is project root
        ssl_dir = base_dir / 'bank_project' / 'ssl' / sql_user

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
            conn = pymysql.connect(
                host=sql_instance,
                user=sql_user,
                password=sql_pass,
                database='bank_db',
                ssl={
                    'ca': str(ssl_ca),
                    'cert': str(ssl_cert),
                    'key': str(ssl_key),
                    'check_hostname': False
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


# def get_sql_logs(request):
#     client = logging_v2.LoggingServiceV2Client()

#     project_id = "your-project-id"
#     log_filter = """
#         resource.type="cloudsql_database"
#         logName="projects/your-project-id/logs/mysql-general.log"
#     """

#     request_logs = {
#         "resource_names": [f"projects/{project_id}"],
#         "filter": log_filter,
#         "order_by": "timestamp desc",
#         "page_size": 10
#     }

#     entries = client.list_log_entries(request_logs)

#     logs = []
#     for entry in entries:
#         logs.append({
#             "timestamp": entry.timestamp.ToJsonString(),
#             "text": entry.text_payload
#         })

#     return JsonResponse({"logs": logs})
