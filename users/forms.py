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


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['user', 'employee_id', 'department', 'first_name', 'last_name', 'national_id', 'phone_number', 'salary']
