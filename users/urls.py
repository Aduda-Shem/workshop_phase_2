from django.urls import path
from django.db.models import Sum

from ecommerce.views import CategoryView, ProductView, SubcategoryView, complete_sale, get_subcategories, pos_view
from .views import  DashboardView, SupplierEditView, SupplierListView, create_employee, employee_list, login

urlpatterns = [
    path('login/', login, name='login'),
    path('', DashboardView.as_view(), name='dashboard'),

    # URLs for managing Suppliers
    path('suppliers/', SupplierListView.as_view(), name='supplier_list'),
    path('suppliers/edt/<int:supplier_id>/', SupplierEditView.as_view(), name='supplier_edit'),

    # URLs for managing Employee
    path('create_employee/', create_employee, name='create_employee'),
    path('employee_list/', employee_list, name='employee_list'),

    # URLs for managing categories
    path('categories/', CategoryView.as_view(), name='category_list'),
    path('categories/create/', CategoryView.as_view(), name='create_category'),
    path('categories/update/<int:pk>/', CategoryView.as_view(), name='update_category'),
    path('categories/delete/<int:pk>/', CategoryView.as_view(), name='delete_category'),


    # URL patterns for managing subcategories within a specific category
    path('category/<int:category_id>/subcategories/', SubcategoryView.as_view(), name='subcategory_category'),
    path('category/<int:category_id>/subcategories/add/', SubcategoryView.as_view(), name='add_subcategory'),
    path('category/<int:category_id>/subcategories/<int:subcategory_id>/edit/', SubcategoryView.as_view(), name='edit_subcategory'),
    path('category/<int:category_id>/subcategories/<int:subcategory_id>/delete/', SubcategoryView.as_view(), name='delete_subcategory'),
    
    # URLs for managing products
    path('products/', ProductView.as_view(), name='product_list'),
    path('products/create/', ProductView.as_view(), {'action': 'create'}, name='create_product'),
    path('products/update/<int:pk>/', ProductView.as_view(), {'action': 'update'}, name='update_product'),
    path('products/delete/<int:pk>/', ProductView.as_view(), {'action': 'delete'}, name='delete_product'),
    path('products/statistics/', ProductView.as_view(), {'action': 'statistics'}, name='product_statistics'),
    path('get_subcategories/', get_subcategories, name='get_subcategories'),

        
    path('pos/', pos_view, name='pos_view'),
    path('complete-sale/', complete_sale, name='complete_sale'),

]