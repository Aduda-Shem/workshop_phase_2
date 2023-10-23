import json
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.db.models import Sum
from .models import Category, PointOfSale, Product, SaleRecord, Subcategory
from .forms import CategoryForm, ProductForm, ProductNameForm, ProductSelectionForm, SubcategoryForm
from django.db import transaction

from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from datetime import datetime
from django.db.models import F, ExpressionWrapper, DecimalField

from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
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
    
@method_decorator(login_required, name='dispatch')
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

        return redirect('add_subcategory', category_id=category.id)

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
        return redirect('add_subcategory', category_id=category.id)


@method_decorator(login_required, name='dispatch')
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
            print(form.is_valid)
            if form.is_valid():
                product = form.save()
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

@method_decorator(login_required, name='dispatch')
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

    product_name_form = ProductNameForm()
    products = Product.objects.all()

    if request.method == 'POST':
        form = ProductSelectionForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product_name']
            quantity = form.cleaned_data['quantity']

            if product.stock_quantity >= quantity:
                cart_item = {
                    'product': product,
                    'quantity': quantity,
                    'subtotal': product.price * quantity,
                }
                cart.append(cart_item)
                total += cart_item['subtotal']

                product.stock_quantity -= quantity
                product.save()

    return render(request, 'sales/selling_point.html', {'cart': cart, 'total': total, 'products': products, 'product_name_form': product_name_form})


def complete_sale(request):
    if request.method == 'POST':
        cart_data = json.loads(request.body.decode('utf-8'))

        if cart_data:
            try:
                with transaction.atomic():
                    point_of_sale = PointOfSale.objects.create(
                        seller=request.user,
                        customer=request.user,
                        payment_method="Cash"
                    )

                    for cart_item in cart_data:
                        product_id = cart_item['product_id']
                        quantity = cart_item['quantity']
                        selling_price = cart_item.get('selling_price')  # Get custom selling price if provided

                        product = Product.objects.get(id=product_id)

                        if product.stock_quantity >= quantity:
                            if selling_price is not None:
                                # If a custom selling price is provided, use it to calculate the total amount
                                total_amount = selling_price * quantity
                            else:
                                # If no custom selling price is provided, use the product's default selling price
                                total_amount = product.price * quantity  # Use 'price' instead of 'selling_price'

                            SaleRecord.objects.create(
                                point_of_sale=point_of_sale,
                                product=product,
                                quantity_sold=quantity,
                                total_amount=total_amount,
                                selling_price=selling_price  # Store the selling price in the SaleRecord
                            )

                            product.stock_quantity -= quantity
                            product.save()
                        else:
                            return JsonResponse({'success': False, 'error_message': 'Insufficient stock'})

                return JsonResponse({'success': True})

            except Exception as e:
                return JsonResponse({'success': False, 'error_message': str(e)})

    return JsonResponse({'success': False, 'error_message': 'Invalid request'})


# REPORTING
@login_required
def stock_report(request):
    products = Product.objects.all()
    report_title = "Stock Report"
    
    context = {
        'data': products,  
        'report_title': report_title,
    }
    return render(request, 'reporting/stock_report.html', context)

@login_required
def best_selling_product_report(request):
    best_selling_products = SaleRecord.objects.values('product__name').annotate(total_quantity_sold=Sum('quantity_sold')).order_by('-total_quantity_sold')
    report_title = "Best Selling Product Report"
    
    context = {
        'data': best_selling_products,  
        'report_title': report_title,
    }
    print(context)
    return render(request, 'reporting/best_selling_report.html', context)

@login_required
def employee_performance_report(request):
    employee_sales = SaleRecord.objects.values('point_of_sale__seller__id', 'point_of_sale__seller__first_name', 'point_of_sale__seller__last_name').annotate(total_quantity_sold=Sum('quantity_sold')).order_by('-total_quantity_sold')
    
    report_title = "Employee Performance Report"
    
    context = {
        'data': employee_sales,  
        'report_title': report_title,
    }
    return render(request, 'reporting/employee_performance_report.html', context)

class StatisticsView(TemplateView):
    template_name = 'product/statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        products = Product.objects.all()
        total_products = len(products)
        total_price_sum = sum(product.price for product in products)
        average_price = total_price_sum / total_products if total_products > 0 else 0

        context['title'] = 'Product Statistics'
        context['total_products'] = total_products
        context['total_price_sum'] = total_price_sum
        context['average_price'] = average_price

        return context
    

from datetime import date

def product_sales_report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Set default values to today's date if start_date and end_date are None
    if start_date is None:
        start_date = date.today()
    if end_date is None:
        end_date = date.today()

    data = SaleRecord.objects.values(
        'point_of_sale__seller__id', 
        'point_of_sale__seller__first_name', 
        'point_of_sale__seller__last_name'
    ).annotate(total_quantity_sold=Sum('quantity_sold')).order_by('-total_quantity_sold')

    for item in data:
        selling_price = F('point_of_sale__product__price')
        purchase_price = F('point_of_sale__product__purchase_price')
        profit_loss_expr = ExpressionWrapper(
            selling_price - purchase_price, 
            output_field=DecimalField(max_digits=10, decimal_places=2)
        )
        item['profit_or_loss'] = SaleRecord.objects.filter(
            point_of_sale__seller__id=item['point_of_sale__seller__id'],
            point_of_sale__sale_datetime__date__gte=start_date,
            point_of_sale__sale_datetime__date__lte=end_date
        ).annotate(profit_or_loss=profit_loss_expr).aggregate(Sum('profit_or_loss'))['profit_or_loss__sum']

    report_title = "Product Sales Report"

    context = {
        'data': data,
        'report_title': report_title,
    }

    return render(request, 'reporting/product_sales_report.html', context)