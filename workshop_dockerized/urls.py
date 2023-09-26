"""myworkshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from inventory.views import add_category, add_item, add_to_cart, category_detail, checkout, delete_category, delete_subcategory, generate_receipt, get_items_by_subcategory, index, inventory_items, remove_from_cart, selling_point, update_category, update_subcategory, view_subcategory

from users.views import CustomLoginView, activate_account, add_supplier, autocomplete_companies, dashboard, delete_supplier, edit_supplier, employee_detail, list_suppliers, register_admin, register_employee, staff_dashboard, update_profile

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register_admin, name='register_admin'),
    path('activate/<str:activation_code>/', activate_account, name='activate_account'),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),

    # After succesful logins
    path('', dashboard, name='dashboard'),
    path('staff_dashboard', staff_dashboard, name='staff_dashboard'),
    path('index', index, name='index'),

    # Urls for category
    path('category/', add_category, name='add_category'),
    path('category/update/<int:category_id>/', update_category, name='update_category'),
    path('category/delete/<int:category_id>/', delete_category, name='delete_category'),

    path('category_detail/<int:category_id>/', category_detail, name='category_detail'),
    path('category/<int:category_id>/subcategory/<int:subcategory_id>/', view_subcategory, name='view_subcategory'),
    path('update_subcategory/<int:category_id>/<int:subcategory_id>/', update_subcategory, name='update_subcategory'),
    path('delete_subcategory/<int:category_id>/<int:subcategory_id>/', delete_subcategory, name='delete_subcategory'),

    path('add-item/', add_item, name='add_item'),
    path('inventory/', inventory_items, name='inventory_items'),
    path('get_items_by_subcategory/<int:subcategory_id>/', get_items_by_subcategory, name='get_items_by_subcategory'),



    #Employee details
    path('register-employee/', register_employee, name='register_employee'),
    path('employee/', employee_detail, name='employee_detail'),

    # Profile
    path('update_profile/', update_profile, name='update_profile'),

    path('add_supplier/', add_supplier, name='add_supplier'),
    path('suppliers/', list_suppliers, name='list_suppliers'),
    path('suppliers/<int:supplier_id>/', list_suppliers, name='list_suppliers_with_id'),
    path('suppliers/edit/<int:supplier_id>/', edit_supplier, name='edit_supplier'),
    path('suppliers/delete/<int:supplier_id>/', delete_supplier, name='delete_supplier'),
    path('autocomplete_companies/', autocomplete_companies, name='autocomplete_companies'),

    # Sales
    path('selling-point/', selling_point, name='selling_point'),
    path('add-to-cart/<int:item_id>/', add_to_cart, name='add_to_cart'),
    path('checkout/', checkout, name='checkout'),
    path('remove-from-cart/', remove_from_cart, name='remove_from_cart'),
    path('generate-receipt/', generate_receipt, name='generate_receipt'),
]



if settings.DEBUG:
    urlpatterns += [path('__debug__/', include("debug_toolbar.urls"))]
    urlpatterns += static(settings.MEDIA_URL, 
                          document_root=settings.MEDIA_ROOT)