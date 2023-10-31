from django.urls import path
from django.db.models import Sum
from ecommerce import views

from ecommerce.views import CategoryDeleteView, CategoryView, DeleteSubcategoryView, ProductView, StatisticsView, SubcategoryView, best_selling_product_report, complete_sale, employee_performance_report, get_subcategories, pos_view, product_sales_report, stock_report
from .views import  DashboardView, SupplierDeleteView, SupplierEditView, SupplierListView, UserProfileView, activate_employee, create_employee, edit_employee, employee_list, login, logout, suspend_employee

urlpatterns = [
    path('accounts/login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('', DashboardView.as_view(), name='dashboard'),

    # URLs for managing Suppliers
    path('suppliers/', SupplierListView.as_view(), name='supplier_list'),
    path('suppliers/add/', SupplierListView.as_view(), name='supplier_add'),
    path('suppliers/edit/<int:pk>/', SupplierListView.as_view(), name='supplier_edit'),
    path('suppliers/delete/<int:pk>/', SupplierDeleteView.as_view(), name='supplier_delete_ajax'),
    
    # URLs for managing Employee
    path('create_employee/', create_employee, name='create_employee'),
    path('employee_list/', employee_list, name='employee_list'),
    path('suspend_employee/<str:employee_id>/', suspend_employee, name='suspend_employee'),
    path('activate_employee/<str:employee_id>/', activate_employee, name='activate_employee'),
    path('edit_employee/<str:employee_id>/', edit_employee, name='edit_employee'),


    # URLs for managing categories
    path('categories/', CategoryView.as_view(), name='category_list'),
    path('categories/create/', CategoryView.as_view(), name='create_category'),
    path('categories/update/<int:pk>/', CategoryView.as_view(), name='update_category'),
    path('categories/delete/<int:pk>/', CategoryDeleteView.as_view(), name='delete_category'),


    # URL patterns for managing subcategories within a specific category
    path('category/<int:category_id>/subcategories/', SubcategoryView.as_view(), name='subcategory_category'),
    path('category/<int:category_id>/subcategories/add/', SubcategoryView.as_view(), name='add_subcategory'),
    path('category/<int:category_id>/subcategories/<int:subcategory_id>/edit/', SubcategoryView.as_view(), name='edit_subcategory'),
    path('subcategories/<int:subcategory_id>/delete/', DeleteSubcategoryView.as_view(), name='delete_subcategory'),
    
    # URLs for managing products
    path('products/', ProductView.as_view(), name='product_list'),
    path('products/create/', ProductView.as_view(), {'action': 'create'}, name='create_product'),
    path('products/update/<int:pk>/', ProductView.as_view(), {'action': 'update'}, name='update_product'),
    path('delete_product/<int:pk>/', ProductView.as_view(), {'action': 'delete'}, name='delete_product'),
    path('products/statistics/', ProductView.as_view(), {'action': 'statistics'}, name='product_statistics'),
    path('get_subcategories/', views.get_subcategories, name='get_subcategories'),

        
    path('pos/', pos_view, name='pos_view'),
    path('complete-sale/', complete_sale, name='complete_sale'),


    # reporting
    path('stock-report/', stock_report, name='stock_report'),
    path('best-selling-product-report/', best_selling_product_report, name='best_selling_product_report'),
    path('employee-performance/', employee_performance_report, name='employee_performance_report'),
    path('product-sales-report/', product_sales_report, name='product_sales_report'),


    path('statistics/', StatisticsView.as_view(), name='statistics'),

]
