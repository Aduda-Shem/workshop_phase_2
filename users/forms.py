from django import forms
from users.models import Supplier, User
from django.contrib.auth.forms import AuthenticationForm


class AdminRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ['first_name','last_name','email', 'phone_number', 'national_id', 'password']

    def __init__(self, *args, **kwargs):
        super(AdminRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'First Name'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Last_Name'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Phone Number'})
        self.fields['national_id'].widget.attrs.update({'class': 'form-control', 'placeholder': 'National ID'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already in use.')
        return email



class EmployeeRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ['first_name','last_name', 'email', 'phone_number', 'national_id']


class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'


class SupplierForm(forms.ModelForm):
    company = forms.CharField(max_length=100, required=False)

    class Meta:
        model = Supplier
        fields = ['name', 'contact_person', 'email', 'phone_number', 'address', 'supplies']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company'].widget.attrs.update({'id': 'companyInput', 'autocomplete': 'on'})


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'national_id', 'image']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        return phone_number



