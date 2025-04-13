from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.about_page, name='about'),
    path('sql-dashboard/',views.sql_dashboard, name='sql_dashboard'),
]


