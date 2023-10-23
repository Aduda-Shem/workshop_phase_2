from datetime import date
from django.views.generic import TemplateView
import json
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from ecommerce.models import Category, Product, SaleRecord

from users.forms import EmployeeForm, LoginForm, SupplierForm
from .models import Company, Employee, Supplier, User

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
from django.urls import reverse

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse


from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib import messages

from decimal import Decimal
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth import get_user_model

import random
import string
import decimal


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

@method_decorator(login_required, name='dispatch')
def logout(request):
    auth_logout(request)
    messages.success(request, f"Successfully logged out")
    return redirect('login')


@method_decorator(login_required, name='dispatch')
class UserProfileView(View):
    template_name = 'users/user_profile.html'

    def get(self, request):
        user = request.user
        context = {
            'user': user,
        }
        return render(request, self.template_name, context)


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)

@method_decorator(login_required, name='dispatch')
class DashboardView(View):
    def get(self, request):
        is_staff = request.user.is_staff

        total_price_all_products = sum(product.price * product.stock_quantity for product in Product.objects.all())
        employee_count = Employee.objects.count()
        supplier_count = Supplier.objects.count()

        today_sale = 0
        recent_sales = []

        if is_staff:
            try:
                employee = request.user.employee
                print("employee_id", employee.id)
                today_sale = SaleRecord.objects.filter(
                    point_of_sale__seller_id=employee.user.id,
                    point_of_sale__sale_datetime__date=date.today()
                ).aggregate(total_sales=Sum('total_amount'))['total_sales'] or 0
                recent_sales = SaleRecord.objects.filter(point_of_sale__seller_id=employee.user.id).order_by('-sale_datetime')[:5]
            except ObjectDoesNotExist:
                pass
        else:
            today_sale = SaleRecord.objects.filter(point_of_sale__sale_datetime__date=date.today()).aggregate(total_sales=Sum('total_amount'))['total_sales'] or 0
            recent_sales = SaleRecord.objects.order_by('-sale_datetime')[:5]

        today = date.today()
        first_day_of_year = date(today.year, 1, 1)

        sales_data = SaleRecord.objects.filter(
            point_of_sale__sale_datetime__date__gte=first_day_of_year
        ).values('point_of_sale__sale_datetime__month').annotate(total_sales=Sum('total_amount'))
        
        labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        
        sales_values = [0] * 12
        
        for sale in sales_data:
            month_index = sale['point_of_sale__sale_datetime__month'] - 1
            sales_values[month_index] = sale['total_sales']
        
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

        context = {
            'total_price_all_products': total_price_all_products,
            'today_sale': today_sale,
            'supplier': supplier_count,
            'employee_count': employee_count,
            'categories': categories,
            'categories_with_total_stock': categories_with_total_stock,
            'recent_sales': recent_sales,
            'sales_chart_data': json.dumps(sales_chart_data, cls=DecimalEncoder),
        }

        return render(request, 'dashboard.html', context)
    
@method_decorator(login_required, name='dispatch')
class SupplierListView(TemplateView):
    template_name = 'suppliers/supplier_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['suppliers'] = Supplier.objects.all()
        context['form'] = SupplierForm()
        return context

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
            context = self.get_context_data()
            return self.render_to_response(context)

    def put(self, request, pk):
        supplier = get_object_or_404(Supplier, pk=pk)
        data = request.POST
        form = SupplierForm(data, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('supplier_list') 
        else:
            context = self.get_context_data()
            context['form'] = form
            return self.render_to_response(context)

    def delete(self, request, pk):
        supplier = get_object_or_404(Supplier, pk=pk)
        supplier.delete()
        return redirect('supplier_list')

    def get_success_url(self):
        return reverse('supplier_list')


class SupplierDeleteView(View):
    def delete(self, request, pk):
        supplier = get_object_or_404(Supplier, pk=pk)
        supplier.delete()
        return JsonResponse({'message': 'Supplier deleted successfully'})

@method_decorator(login_required, name='dispatch')
class SupplierEditView(LoginRequiredMixin, View):
    template_name = 'suppliers/supplier_list.html'

    def get(self, request, supplier_id):
        supplier = get_object_or_404(Supplier, id=supplier_id)
        form = SupplierForm(instance=supplier)
        context = {
            'form': form,
            'supplier': supplier,
        }
        return render(request, self.template_name, context)
    
    def post(self, request, supplier_id):
        supplier = get_object_or_404(Supplier, id=supplier_id)
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            messages.success(request, f"Supplier edited successfully.")
            return redirect('supplier_list')
        
        context = {
            'form': form,
            'supplier': supplier,
        }
        return render(request, self.template_name, context)
    

@method_decorator(login_required, name='dispatch')
def create_employee(request):
    if request.method == 'POST':
        employee_form = EmployeeForm(request.POST)
        if employee_form.is_valid():
            User = get_user_model()

            username = generate_unique_username(employee_form.cleaned_data['email'])
            password = generate_password()

            user = User(
                email=employee_form.cleaned_data['email'],
                username=username,
                is_staff=True,
            )
            user.set_password(password)
            user.save()

            employee = Employee(
                user=user,
                employee_id=generate_employee_id(employee_form.cleaned_data['national_id']),
                first_name=employee_form.cleaned_data['first_name'],
                last_name=employee_form.cleaned_data['last_name'],
                national_id=employee_form.cleaned_data['national_id'],
                phone_number=employee_form.cleaned_data['phone_number'],
                salary=employee_form.cleaned_data['salary'],
            )
            employee.save()

            subject = 'Welcome to Our Company'
            html_message = render_to_string('email/welcome_email_template.html', {'employee': employee})
            plain_message = strip_tags(html_message)
            from_email = 'noreply@netbotgroup.com'
            to_email = user.email

            send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)

            messages.success(request, 'Employee created successfully, and a welcome email has been sent.')
            return redirect('create_employee')
        else:
            print("Form is not valid:", employee_form.errors)
    else:
        employee_form = EmployeeForm()

    return render(request, 'users/add_employee.html', {'employee_form': employee_form})

def generate_employee_id(national_id):
    if len(national_id) >= 4:
        last_4_digits = national_id[-4:]
        return last_4_digits
    else:
        return None

def generate_password():
    password_length = 8
    characters = string.ascii_lowercase + string.digits
    password = ''.join(random.choice(characters) for _ in range(password_length))
    return password

def generate_unique_username(email):
    username = email.split('@')[0]
    return username


@login_required
def employee_list(request):
    employees = Employee.objects.all()  
    print("employees",employees)
    return render(request, 'users/view_employee.html', {'employees': employees})

@login_required
def suspend_employee(request, employee_id):
    employee = get_object_or_404(Employee, employee_id=employee_id)
    if employee.user.is_active:
        employee.user.is_active = False
        employee.user.save()
        messages.success(request, f'Suspended {employee.first_name} {employee.last_name}.')
    return redirect('employee_list')

@login_required
def activate_employee(request, employee_id):
    employee = get_object_or_404(Employee, employee_id=employee_id)
    if not employee.user.is_active:
        employee.user.is_active = True
        employee.user.save()
        messages.success(request, f'Activated {employee.first_name} {employee.last_name}.')
    return redirect('employee_list')


@login_required
def edit_employee(request, employee_id):
    employee = get_object_or_404(Employee, employee_id=employee_id)

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee details updated successfully.')
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)

    return render(request, 'edit_employee.html', {'form': form, 'employee': employee})