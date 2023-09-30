# forms.py
from django import forms
from .models import Category, Subcategory

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Category Description'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subcategory Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Subcategory Description'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
        }
