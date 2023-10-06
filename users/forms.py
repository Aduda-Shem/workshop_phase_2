# forms.py
from django import forms
from .models import Employee, Supplier
from django.core.validators import EmailValidator

class LoginForm(forms.Form):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Enter your email', 'class': 'custom-email-input form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password', 'class': 'prompt srch_explore form-control'}))

        
class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'


class EmployeeForm(forms.Form):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(
        label='Email Address',
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        validators=[EmailValidator(message='Enter a valid email address.')],
        required=True
    )
    phone_number = forms.CharField(max_length=100, required=True)
    national_id = forms.CharField(max_length=8, required=True)
    salary = forms.DecimalField(max_digits=10, decimal_places=2, required=True)

