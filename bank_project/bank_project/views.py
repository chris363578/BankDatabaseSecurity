# /Users/bigdata12/projects/BankDatabaseSecurity/bank_project/bank_project/views.py

from django.shortcuts import render

def homepage_view(request):
    """
    Renders the project's main homepage.
    Looks for the template 'homepage.html' in directories specified
    in settings.TEMPLATES['DIRS'] or app template directories.
    """
  
    return render(request, 'homepage.html')

