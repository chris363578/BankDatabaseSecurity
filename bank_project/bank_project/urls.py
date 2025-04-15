# /Users/bigdata12/projects/BankDatabaseSecurity/bank_project/bank_project/urls.py
"""
URL configuration for bank_project project.
"""
from django.contrib import admin
from django.urls import path, include
# Import the new project-level view
from . import views as project_views # Use 'as' to avoid name clashes if needed

urlpatterns = [
    # Admin site URL
    path('admin/', admin.site.urls),

    # Homepage URL (Root path '')
    path('', project_views.homepage_view, name='homepage'), # Points to the new view

    # Include URLs from the 'bank' app under the '/bank/' prefix
    # This means login will be at /bank/login/, dashboard at /bank/dashboard/, etc.
    path('bank/', include('bank.urls')),

    # You might need other project-wide URLs here later
]
