from django.core.management.base import BaseCommand
from django.utils import timezone
from random import randint, choice, uniform
from datetime import datetime, timedelta
from bank.models import Customer, Account, Transaction, Employee
import faker

class Command(BaseCommand):
    help = 'Populates the database with sample banking data'

    def handle(self, *args, **options):
        self.stdout.write('Starting database population...')
        
        # Initialize faker for generating realistic data
        fake = faker.Faker()
        
        # Create Customers
        self.stdout.write('Creating customers...')
        customers = []
        for i in range(1, 21):  # Create 20 customers
            customer = Customer(
                customer_id=i,
                customer_name=fake.name(),
                email=fake.email(),
                date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=90),
                date_joined=timezone.make_aware(fake.date_time_between(start_date='-5y', end_date='now'))
            )
            # Set encrypted fields
            customer.set_encrypted_field('phone_number', fake.phone_number()[:15])  # Limit length to avoid DB overflow
            customer.set_encrypted_field('address', fake.address())
            customer.set_encrypted_field('ssn', f"{randint(100, 999)}-{randint(10, 99)}-{randint(1000, 9999)}")
            
            customer.save()
            customers.append(customer)
            self.stdout.write(f'  - Created customer: {customer}')
        
        # Create Accounts
        self.stdout.write('Creating accounts...')
        accounts = []
        account_id = 1
        for customer in customers:
            # Each customer gets 1-3 accounts
            for _ in range(randint(1, 3)):
                # Make sure date_opened is timezone-aware
                date_opened = timezone.make_aware(fake.date_time_between(
                    start_date=customer.date_joined,
                    end_date=timezone.now()
                ))
                
                account = Account(
                    account_id=account_id,
                    customer=customer,
                    account_type=choice(['checking', 'savings', 'business']),
                    date_opened=date_opened
                )
                # Set encrypted balance (between $100 and $50,000)
                account.set_balance(round(uniform(100, 50000), 2))
                
                account.save()
                accounts.append(account)
                self.stdout.write(f'  - Created account: {account}')
                account_id += 1
        
        # Create Transactions
        self.stdout.write('Creating transactions...')
        transaction_id = 1
        for account in accounts:
            # Each account gets 5-15 transactions
            for _ in range(randint(5, 15)):
                # Generate transaction amount ($10-$2000)
                amount = round(uniform(10, 2000), 2)
                
                # Make sure transaction_date is timezone-aware
                transaction_date = timezone.make_aware(fake.date_time_between(
                    start_date=account.date_opened,
                    end_date=timezone.now()
                ))
                
                transaction = Transaction(
                    transaction_id=transaction_id,
                    account=account,
                    transaction_type=choice(['deposit', 'withdrawl', 'transfer', 'payment']),
                    amount=amount,
                    transaction_date=transaction_date,
                    transaction_description=fake.sentence()
                )
                transaction.save()
                self.stdout.write(f'  - Created transaction: {transaction}')
                transaction_id += 1
        
        # Create Employees
        self.stdout.write('Creating employees...')
        for i in range(1, 11):  # Create 10 employees
            # Format phone number to ensure it's within 15 characters
            formatted_phone = fake.numerify(text="###-###-####")  # Creates a standard US phone format
            
            hire_date = fake.date_between(start_date='-10y', end_date='-1m')
            
            employee = Employee(
                employee_id=i,
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.company_email(),
                phone=formatted_phone,  # Using the formatted phone number
                hire_date=hire_date,
                e_role=choice(['banker', 'advisor', 'manager', 'reception'])
            )
            employee.save()
            self.stdout.write(f'  - Created employee: {employee}')
        
        self.stdout.write(self.style.SUCCESS('Successfully populated database with sample data!'))