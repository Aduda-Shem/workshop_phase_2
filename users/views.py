import random
import string
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse, reverse_lazy
from inventory.models import Category, Item
from django.contrib.auth.decorators import login_required

from django.views.decorators.http import require_http_methods
from django.contrib.auth.forms import UserChangeForm



from users.forms import AdminRegistrationForm, CustomLoginForm, EmployeeRegistrationForm, ProfileUpdateForm, SupplierForm
from users.models import Company, Supplier, User
from django.db.models import F, Sum
from users.utils import send_registration_email

def register_admin(request):
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.is_admin = True
            password = generate_random_password()
            user.password = make_password(password)
            user.activation_code = generate_activation_code()
            user.save()
            send_activation_email(request, user, password)
            return redirect('login')
    else:
        form = AdminRegistrationForm()
    return render(request, 'users/register_admin.html', {'form': form})

def generate_random_password():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(8))


def generate_activation_code():
    length = 10
    code = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    return code


def send_activation_email(request, user, password):
    activation_link = request.build_absolute_uri(reverse('activate_account', args=[user.activation_code]))
    subject = 'Activate your account'
    message = f'Please click the following link to activate your account: {activation_link}\n\n'
    message += f'Your generated password is: {password}\n\n'
    message += 'Please keep this information secure.'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)


def activate_account(request, activation_code):
    try:
        user = User.objects.get(activation_code=activation_code)
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated. You can now log in.')
        return redirect('login')
    except User.DoesNotExist:
        messages.error(request, 'Invalid activation code.')
        return redirect('activation_error')

#Employee Registeration
def register_employee(request):
    if request.method == 'POST':
        form = EmployeeRegistrationForm(request.POST)
        print(form)
        if form.is_valid():
            print(form.is_valid)
            user = form.save(commit=False)
            user.is_active = True
            user.is_staff = True
            password = generate_random_password()
            user.set_password(password)
            user.save()
            send_registration_email(request, user, password)
            return redirect('employee_detail')
    else:
        form = EmployeeRegistrationForm()
    return render(request, 'users/add_employee.html', {'form': form})


# class CustomLoginView(LoginView):
#     template_name = 'users/user_login.html'
#     success_url = '/home/'
#     authentication_form = CustomLoginForm

class CustomLoginView(LoginView):
    template_name = 'users/user_login.html'
    success_url = reverse_lazy('home')
    authentication_form = CustomLoginForm

    def get_success_url(self):
        if self.request.user.is_staff:
            return reverse_lazy('staff_dashboard')
        else:
            return super().get_success_url()



@login_required
def dashboard(request):
    user = request.user
    categories = Category.objects.all()
    items = Item.objects.all()
    supplier = Supplier.objects.count() 
    total_quantity = Item.objects.aggregate(total_quantity=Sum('quantity'))['total_quantity']
    total_price = Item.objects.annotate(
        total_item_price=F('quantity') * F('price')
    ).aggregate(total_price_sum=Sum('total_item_price'))['total_price_sum']
    employee = User.objects.filter(is_staff=True).count()
    categories_with_total_stock = Category.objects.annotate(
        total_stock=Sum('subcategory__item__quantity'),
        total_price=Sum('subcategory__item__price')
    )

    context = {
        'user': user,
        'supplier': supplier,
        'items': items,
        'categories': categories,
        'employee': employee,
        'total_price': total_price,
        'total_quantity': total_quantity,
        'categories_with_total_stock': categories_with_total_stock,
    }

    return render(request, 'dashboard.html', context)

@login_required
def staff_dashboard(request):
    user = request.user
    categories = Category.objects.all()
    supplier = Supplier.objects.count() 
    total_quantity = Item.objects.aggregate(total_quantity=Sum('quantity'))['total_quantity']
    total_price = Item.objects.annotate(
        total_item_price=F('quantity') * F('price')
    ).aggregate(total_price_sum=Sum('total_item_price'))['total_price_sum']
    employee = User.objects.filter(is_staff=True).count()
    categories_with_total_stock = Category.objects.annotate(
        total_stock=Sum('subcategory__item__quantity'),
        total_price=Sum('subcategory__item__price')
    )

    context = {
        'user': user,
        'supplier': supplier,
        'categories': categories,
        'employee': employee,
        'total_price': total_price,
        'total_quantity': total_quantity,
        'categories_with_total_stock': categories_with_total_stock,
    }

    return render(request, 'staff_dashboard.html', context)


@login_required
def employee_detail(request):
    employees =  User.objects.filter(is_staff=True)
    return render(request, 'users/view_employee.html', {'employees': employees})


@login_required
def update_profile(request):
    if request.method == 'POST':
        user_form = UserChangeForm(request.POST, request.FILES, instance=request.user)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, f'Your profile has been updated!')
            return redirect('update_profile')

    else:
        user_form = UserChangeForm(instance=request.user)

    context = {
        'user_form': user_form,
    }
    return render(request, 'users/user_profile.html', context)



@login_required
def add_supplier(request):
    if request.method == "POST":
        form = SupplierForm(request.POST)
        if form.is_valid():
            # Save Supplier details without committing to the database yet
            supplier = form.save(commit=False)

            # Check if the company exists, if not, create it
            company_name = form.cleaned_data.get('company')
            if company_name:
                company, created = Company.objects.get_or_create(name=company_name)
                supplier.company = company

            # Save the supplier to the database
            supplier.save()
            return redirect('list_suppliers')
    else:
        form = SupplierForm()
    return render(request, 'suppliers/add_supplier.html', {'form': form})



@login_required
def list_suppliers(request, supplier_id=None):
    suppliers = Supplier.objects.all()

    if supplier_id:
        supplier = get_object_or_404(Supplier, id=supplier_id)
    else:
        supplier = None

    return render(request, 'suppliers/list_suppliers.html', {'suppliers': suppliers, 'supplier': supplier})

def edit_supplier(request, supplier_id):
    supplier = get_object_or_404(Supplier, id=supplier_id)

    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('list_suppliers')
    else:
        form = SupplierForm(instance=supplier)

    return render(request, 'suppliers/edit_supplier.html', {'supplier': supplier, 'form': form})


@require_http_methods(["GET"])
def autocomplete_companies(request):
    term = request.GET.get('term')
    companies = Company.objects.filter(name__icontains=term)[:10]  # Filter companies based on the search term
    results = [company.name for company in companies]
    return JsonResponse(results, safe=False)


@login_required
def delete_supplier(request, supplier_id):
    supplier = get_object_or_404(Supplier, id=supplier_id)

    if request.method == 'POST':
        supplier.delete()
        return redirect('list_suppliers')

    return redirect('list_suppliers')




