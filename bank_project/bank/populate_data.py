from django.db import models
from django.utils import timezone
from cryptography.fernet import Fernet
from django.conf import settings

# Default encryption key if not set in settings
DEFAULT_ENCRYPTION_KEY = b'9aboH821ApzYxbyvRYxqgG1fD9P9wJtjku2-IGO9blg='

class Customer(models.Model):
    customer_id = models.IntegerField(primary_key=True, default=0)
    customer_name = models.CharField(max_length=100, default='name')
    email = models.EmailField(max_length=255, default='email')
    phone_number = models.BinaryField(null=True, blank=True)  # Encrypted
    address = models.BinaryField(null=True, blank=True)      # Encrypted
    date_of_birth = models.DateField(null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    ssn = models.BinaryField(null=True, blank=True)          # Encrypted

    @property
    def cipher(self):
        key = getattr(settings, 'ENCRYPTION_KEY', DEFAULT_ENCRYPTION_KEY)
        return Fernet(key)

    def set_encrypted_field(self, field_name, value):
        if value:
            encrypted_value = self.cipher.encrypt(value.encode())
            setattr(self, field_name, encrypted_value)

    def get_encrypted_field(self, field_name):
        value = getattr(self, field_name)
        if value:
            return self.cipher.decrypt(value).decode()
        return None

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer_name} ({self.customer_id})"

class Account(models.Model):
    ACCOUNT_TYPES = (
        ('checking', 'Checking'),
        ('savings', 'Savings'),
        ('business', 'Business'),
    )
    account_id = models.IntegerField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    balance = models.BinaryField()  # Encrypted
    date_opened = models.DateTimeField(default=timezone.now)

    @property
    def cipher(self):
        key = getattr(settings, 'ENCRYPTION_KEY', DEFAULT_ENCRYPTION_KEY)
        return Fernet(key)

    def set_balance(self, value):
        self.balance = self.cipher.encrypt(str(value).encode())

    def get_balance(self):
        return float(self.cipher.decrypt(self.balance).decode())

    def __str__(self):
        return f"{self.account_id} - {self.account_type}"

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('deposit', 'Deposit'),
        ('withdrawl', 'Withdrawal'),
        ('transfer', 'Transfer'),
        ('payment', 'Payment'),
    )
    transaction_id = models.IntegerField(primary_key=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_date = models.DateTimeField(default=timezone.now)
    transaction_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.transaction_id} - {self.transaction_type}"

class Employee(models.Model):
    ROLES = (
        ('banker', 'Banker'),
        ('advisor', 'Advisor'),
        ('manager', 'Manager'),
        ('reception', 'Reception'),
    )
    employee_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=15, null=True, blank=True)
    hire_date = models.DateField()
    e_role = models.CharField(max_length=20, choices=ROLES)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.employee_id})"