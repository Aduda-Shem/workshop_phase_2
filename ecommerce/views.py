from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from .models import Category, Product, Subcategory
from .forms import CategoryForm, ProductForm, SubcategoryForm

class CategoryView(View):
    template_name = 'category/category_list.html'

    def get(self, request, pk=None):
        if pk:
            category = get_object_or_404(Category, pk=pk)
            return self.get_category_data(request, category)
        else:
            categories = Category.objects.all()
            form = CategoryForm()
            return render(request, self.template_name, {'categories': categories, 'form': form})

    def post(self, request):
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category created successfully.')
        else:
            messages.error(request, 'Category creation failed.')
        return redirect('category_list')

    def put(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        form = CategoryForm(request.POST, request.FILES, instance=category)

        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully.')
        else:
            messages.error(request, 'Category update failed.')
        
        return redirect('category_list')

    def delete(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        messages.success(request, 'Category deleted successfully.')
        return redirect('category_list')

    def get_category_data(self, request, category):
        data = {
            'name': category.name,
            'description': category.description,
            'image_url': category.image.url,
        }
        return JsonResponse(data)
    
class SubcategoryView(View):
    template_name = 'category/subcategory.html'

    def get(self, request, category_id):
        category = get_object_or_404(Category, pk=category_id)
        subcategories = Subcategory.objects.filter(category=category)
        context = {
            'category': category,
            'subcategories': subcategories,
        }
        return render(request, self.template_name, context)

    def post(self, request, category_pk):
        category = get_object_or_404(Category, pk=category_pk)
        subcategory_form = SubcategoryForm(request.POST, request.FILES)

        if subcategory_form.is_valid():
            subcategory = subcategory_form.save(commit=False)
            subcategory.category = category
            subcategory.save()
            messages.success(request, 'Subcategory created successfully.')
        else:
            messages.error(request, 'Subcategory creation failed.')

        return redirect('category_list')

    def put(self, request, subcategory_pk):
        subcategory = get_object_or_404(Subcategory, pk=subcategory_pk)
        form = SubcategoryForm(instance=subcategory)

        if request.method == 'POST':
            form = SubcategoryForm(request.POST, request.FILES, instance=subcategory)
            if form.is_valid():
                form.save()
                messages.success(request, 'Subcategory updated successfully.')
                return redirect('category_list')
            else:
                messages.error(request, 'Subcategory update failed.')

        return render(request, self.template_name, {'form': form})

    def delete(self, request, subcategory_pk):
        subcategory = get_object_or_404(Subcategory, pk=subcategory_pk)
        subcategory.delete()
        messages.success(request, 'Subcategory deleted successfully.')
        return redirect('category_list')



class ProductView(View):
    template_name = 'product/product_list.html'

    def get(self, request):
        products = Product.objects.all()
        form = ProductForm()
        return render(request, self.template_name, {'products': products, 'form': form})

    def post(self, request):
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product created successfully.')
        else:
            messages.error(request, 'Product creation failed.')
        return redirect('product_list')

    def put(self, request):
        product_id = request.POST.get('pk')
        product = get_object_or_404(Product, pk=product_id)
        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
        else:
            messages.error(request, 'Product update failed.')
        
        return redirect('product_list')

    def delete(self, request):
        product_id = request.POST.get('pk')
        product = get_object_or_404(Product, pk=product_id)
        product.delete()
        messages.success(request, 'Product deleted successfully.')
        return redirect('product_list')

    def get_product_data(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        data = {
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'stock_quantity': product.stock_quantity,
            'category': product.category.name,
            'subcategory': product.subcategory.name,
            'image_url': product.image.url,
        }
        return JsonResponse(data)
