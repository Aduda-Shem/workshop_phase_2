from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.db.models import Sum
from .models import Category, Product, Subcategory
from .forms import CategoryForm, ProductForm, ProductNameForm, SubcategoryForm

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

    def post(self, request, category_id):
        category = get_object_or_404(Category, pk=category_id)
        subcategory_form = SubcategoryForm(request.POST, request.FILES)

        if subcategory_form.is_valid():
            subcategory = subcategory_form.save(commit=False)
            subcategory.category = category
            subcategory.save()
            messages.success(request, 'Subcategory created successfully.')
        else:
            messages.error(request, 'Subcategory creation failed.')
            print(subcategory_form.errors)

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

    def get(self, request, action=None, pk=None):
        categories = Category.objects.all() 
        subcategories = Subcategory.objects.all()

        if action == 'create':
            form = ProductForm()
            return render(request, self.template_name, {'form': form, 'categories': categories, 'subcategories': subcategories})
        elif action == 'update':
            product = get_object_or_404(Product, pk=pk)
            form = ProductForm(instance=product)
            return render(request, self.template_name, {'form': form, 'product': product, 'categories': categories, 'subcategories': subcategories})
        elif action == 'statistics':
            return self.get_statistics(request)

        products = Product.objects.all()
        form = ProductForm()
        return render(request, self.template_name, {'products': products, 'form': form, 'categories': categories, 'subcategories': subcategories})


    def post(self, request, action=None, pk=None):
        if action == 'create':
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Product created successfully.')
                return redirect('product_list')
            else:
                messages.error(request, 'Product creation failed.')
        elif action == 'update':
            product = get_object_or_404(Product, pk=pk)
            form = ProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()
                messages.success(request, 'Product updated successfully.')
                return redirect('product_list')
            else:
                messages.error(request, 'Product update failed.')
        elif action == 'delete':
            product = get_object_or_404(Product, pk=pk)
            product.delete()
            messages.success(request, 'Product deleted successfully.')
            return redirect('product_list')

        products = Product.objects.all()
        form = ProductForm()
        return render(request, self.template_name, {'products': products, 'form': form})

    def get_statistics(self, request):
        total_products = Product.objects.count()
        total_price_sum = Product.objects.aggregate(total_price_sum=Sum('price'))['total_price_sum']
        average_price = total_price_sum / total_products if total_products > 0 else 0

        statistics_data = {
            'total_products': total_products,
            'total_price_sum': str(total_price_sum),
            'average_price': str(average_price),
        }

        return JsonResponse(statistics_data)

def get_subcategories(request):
    category_id = request.GET.get('category_id')

    if category_id:
        subcategories = Subcategory.objects.filter(category_id=category_id).values('id', 'name')
    else:
        subcategories = []

    return JsonResponse({'subcategories': list(subcategories)})



def pos_view(request):
    cart = []
    total = 0

    if request.method == 'POST':
        form = ProductNameForm(request.POST)
        if form.is_valid():
            product_ids = form.cleaned_data['product_ids']
            products = Product.objects.filter(id__in=product_ids)

            for product in products:
                cart.append(product)
                total += product.price

    products = Product.objects.all()

    return render(request, 'sales/selling_point.html', {'cart': cart, 'total': total, 'products': products})