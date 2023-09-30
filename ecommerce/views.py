from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from .models import Category, Subcategory
from .forms import CategoryForm, SubcategoryForm

class CategoryView(View):
    template_name = 'category/category_list.html'

    def get(self, request):
        categories = Category.objects.all()
        form = CategoryForm()
        subcategory_form = SubcategoryForm()
        return render(request, self.template_name, {'categories': categories, 'form': form, 'subcategory_form': subcategory_form})

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
        form = CategoryForm(instance=category)

        if request.method == 'POST':
            form = CategoryForm(request.POST, request.FILES, instance=category)
            if form.is_valid():
                form.save()
                messages.success(request, 'Category updated successfully.')
                return redirect('category_list')
            else:
                messages.error(request, 'Category update failed.')

        return render(request, self.template_name, {'form': form})

    def delete(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        messages.success(request, 'Category deleted successfully.')
        return redirect('category_list')

class SubcategoryView(View):
    template_name = 'category/category_list.html'

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
