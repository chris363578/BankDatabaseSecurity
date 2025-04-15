
from django.urls import path
# Import the views from the bank app's views.py
from . import views as bank_views

# These will be prefixed with '/bank/' by the project urls.py
urlpatterns = [
    # /bank/login/
    path('login/', bank_views.login, name='login_page'),

    # /bank/dashboard/
    path('dashboard/', bank_views.dashboard, name='sql_dashboard'),

    # /bank/logout/
    path('logout/', bank_views.logout, name='logout'),

    # Add other bank-app specific URLs here
]
