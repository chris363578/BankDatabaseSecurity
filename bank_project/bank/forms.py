from django import forms
from .models import Customer, Account

class CustomerAdminForm(forms.ModelForm):
    # Add plain text fields for encrypted data
    phone_number_text = forms.CharField(max_length=15, required=False, label="Phone Number")
    address_text = forms.CharField(widget=forms.Textarea, required=False, label="Address")
    ssn_text = forms.CharField(max_length=11, required=False, label="SSN")
    
    class Meta:
        model = Customer
        fields = ['customer_id', 'customer_name', 'email', 'date_of_birth', 'date_joined']
    
    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        if instance:
            # Populate initial values from encrypted fields
            initial = kwargs.get('initial', {})
            if instance.phone_number:
                initial['phone_number_text'] = instance.get_encrypted_field('phone_number')
            if instance.address:
                initial['address_text'] = instance.get_encrypted_field('address')
            if instance.ssn:
                initial['ssn_text'] = instance.get_encrypted_field('ssn')
            kwargs['initial'] = initial
        super().__init__(*args, **kwargs)
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Encrypt and save data from text fields
        if self.cleaned_data.get('phone_number_text'):
            instance.set_encrypted_field('phone_number', self.cleaned_data['phone_number_text'])
        if self.cleaned_data.get('address_text'):
            instance.set_encrypted_field('address', self.cleaned_data['address_text'])
        if self.cleaned_data.get('ssn_text'):
            instance.set_encrypted_field('ssn', self.cleaned_data['ssn_text'])
        
        if commit:
            instance.save()
        return instance
    

class AccountAdminForm(forms.ModelForm):
    balance_text = forms.DecimalField(max_digits=15, decimal_places=2, required=True, label="Balance")
    
    class Meta:
        model = Account
        fields = ['account_id', 'customer', 'account_type', 'date_opened']
    
    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        if instance and instance.balance:
            initial = kwargs.get('initial', {})
            initial['balance_text'] = instance.get_balance()
            kwargs['initial'] = initial
        super().__init__(*args, **kwargs)
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        if self.cleaned_data.get('balance_text'):
            instance.set_balance(self.cleaned_data['balance_text'])
        
        if commit:
            instance.save()
        return instance
