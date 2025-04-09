from django.contrib import admin
from .models import Customer, Account, Transaction, Employee
from .forms import CustomerAdminForm , AccountAdminForm # Import the form we created

class CustomerAdmin(admin.ModelAdmin):
    form = CustomerAdminForm
    list_display = ('customer_id', 'customer_name', 'email', 'date_joined')
    search_fields = ('customer_name', 'email')



class AccountAdmin(admin.ModelAdmin):
    form = AccountAdminForm
    list_display = ('account_id', 'customer', 'account_type', 'date_opened')
    search_fields = ('account_id', 'customer__customer_name')

admin.site.register(Account, AccountAdmin)

# Register your models with the admin site
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Transaction)
admin.site.register(Employee)