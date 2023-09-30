from datetime import date
import json
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from ecommerce.models import Category, Product, SaleRecord

from users.forms import LoginForm, SupplierForm
from .models import Company, Employee, Supplier

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import date, timedelta
from django.db.models import Sum


# Authentication Views
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password) 
            if user and user.is_active:
                auth_login(request, user)
                messages.success(request, 'Successfully logged in')
                return redirect('dashboard') 
            else:
                messages.error(request, 'Incorrect credentials.')
        else:
            messages.error(request, 'Invalid form submission.')
    else:
        form = LoginForm()
    
    return render(request, 'users/user_login.html', {'form': form})

@login_required
def logout(request):
    auth_logout(request)
    messages.success(request, f"Successfully logged out")
    return redirect('login')


@method_decorator(login_required, name='dispatch')
class DashboardView(View):
    def get(self, request):
        total_price = sum(product.price * product.stock_quantity for product in Product.objects.all())

        employee_count = Employee.objects.count()
        supplier_count = Supplier.objects.count()

        today_sale = SaleRecord.objects.filter(point_of_sale__sale_datetime__date=date.today()).aggregate(total_sales=Sum('total_amount'))['total_sales'] or 0

        today = date.today()
        six_months_ago = today - timedelta(days=180)  

        sales_data = SaleRecord.objects.filter(point_of_sale__sale_datetime__date__gte=six_months_ago) \
            .values('point_of_sale__sale_datetime__month') \
            .annotate(total_sales=Sum('total_amount')) \
            .order_by('point_of_sale__sale_datetime__month')

        labels = [month for month in range(1, 13)] 
        sales_values = [sales['total_sales'] if sales['total_sales'] else 0 for sales in sales_data]

        sales_chart_data = {
            'labels': labels,
            'datasets': [
                {
                    'label': "Monthly Sales",
                    'data': sales_values,
                    'borderColor': "rgba(75, 192, 192, 1)",
                    'borderWidth': 1,
                    'fill': False,
                },
            ],
        }

        categories = Category.objects.all()
        categories_with_total_stock = []
        for category in categories:
            products_in_category = Product.objects.filter(category=category)
            total_stock = sum(product.stock_quantity for product in products_in_category)
            total_price = sum(product.price * product.stock_quantity for product in products_in_category)
            categories_with_total_stock.append({'id': category.id, 'total_stock': total_stock, 'total_price': total_price})

        recent_sales = SaleRecord.objects.order_by('-sale_datetime')[:10]

        context = {
            'total_price': total_price,
            'employee': employee_count,
            'today_sale': today_sale,
            'supplier': supplier_count,
            'categories': categories,
            'categories_with_total_stock': categories_with_total_stock,
            'recent_sales': recent_sales,
            'sales_chart_data': json.dumps(sales_chart_data),
        }

        return render(request, 'dashboard.html', context)

@method_decorator(login_required, name='dispatch')
class SupplierListView(View):
    template_name = 'suppliers/supplier_list.html'

    def get(self, request):
        suppliers = Supplier.objects.all()
        form = SupplierForm()
        return render(request, self.template_name, {'suppliers': suppliers, 'form': form})

    def post(self, request):
        data = request.POST
        form = SupplierForm(data)
        if form.is_valid():
            company_name = data.get('company', None)
            if company_name:
                company, created = Company.objects.get_or_create(name=company_name)
                form.instance.company = company

            form.save()
            return redirect('supplier_list') 
        else:
            suppliers = Supplier.objects.all()
            return render(request, self.template_name, {'suppliers': suppliers, 'form': form})

    def put(self, request, pk):
        supplier = get_object_or_404(Supplier, pk=pk)
        data = request.POST
        form = SupplierForm(data, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('supplier_list') 
        else:
            return render(request, self.template_name, {'form': form})

    def delete(self, request, pk):
        supplier = get_object_or_404(Supplier, pk=pk)
        supplier.delete()
        return redirect('supplier_list')