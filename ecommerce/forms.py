# forms.py
from django import forms
from .models import Category, Product, Subcategory
from django_select2.forms import ModelSelect2MultipleWidget

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Category Description'}),
        }

class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = ('name', 'description', 'category') 
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subcategory Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Subcategory Description'}),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'purchase_price', 'price', 'stock_quantity', 'category', 'subcategory', 'image']



class ProductNameForm(forms.Form):
    product_ids = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all(),
        widget=ModelSelect2MultipleWidget(
            model=Product,
            search_fields=['name__icontains'],
        ),
    )

class ProductSelectionForm(forms.Form):
    product_name = forms.ModelChoiceField(queryset=Product.objects.all(), empty_label="Select a product")
    quantity = forms.IntegerField(min_value=1)
