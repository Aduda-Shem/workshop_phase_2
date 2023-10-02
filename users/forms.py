# forms.py
from django import forms
from .models import Employee, Supplier

class LoginForm(forms.Form):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Enter your email', 'class': 'custom-email-input form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password', 'class': 'prompt srch_explore form-control'}))

        
class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'


class EmployeeForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    national_id = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=100)
    salary = forms.DecimalField(max_digits=10, decimal_places=2)

