# forms.py
from django import forms
from .models import Category, Product, Subcategory

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
        fields = ('name', 'description', 'image', 'category')         
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subcategory Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Subcategory Description'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock_quantity', 'category', 'subcategory', 'image']