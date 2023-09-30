from django.urls import path

from ecommerce.views import CategoryView, SubcategoryView
from .views import  DashboardView, SupplierListView, login

urlpatterns = [
    path('login/', login, name='login'),
    path('', DashboardView.as_view(), name='dashboard'),

    # Supplier URLs
    path('suppliers/', SupplierListView.as_view(), name='supplier_list'),

    # Category
    path('categories/', CategoryView.as_view(), name='category_list'),
    path('categories/<int:pk>/', CategoryView.as_view(), name='category_detail'),
    path('categories/<int:category_pk>/subcategories/', SubcategoryView.as_view(), name='subcategory_list'),

]

