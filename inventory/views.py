from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect

from inventory.forms import CategoryForm, ItemForm, SubcategoryForm
from inventory.models import Cart, CartItem, Category, Item, Subcategory

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.cache import cache
from django.http import JsonResponse
from django.core import serializers
from django.db.models import Prefetch



def index(request):
    return render(request, 'index.html')

# View to handle listing and deleting of category for inventories.
@login_required
def add_category(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_category')
    else:
        form = CategoryForm()

    context = {
        'form': form,
        'categories': categories,
    }

    return render(request, 'inventory/category.html', context)

#View to update Category
@login_required
def update_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = CategoryForm(instance=category)
    
    context = {
        'form': form,
        'category': category,
    }
    
    return render(request, 'update_category.html', context)

# View to delete category 
@login_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    
    if request.method == 'POST':
        category.delete()
        return  redirect('add_category')
    
    context = {
        'category': category,
    }
    
    return render(request, 'delete_category.html', context)



# sub category section
@login_required
def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    subcategories = category.subcategory_set.all()

    if request.method == 'POST':
        if 'add_subcategory' in request.POST:
            subcategory_form = SubcategoryForm(request.POST)
            if subcategory_form.is_valid():
                subcategory = subcategory_form.save(commit=False)
                subcategory.category = category
                subcategory.save()
                return redirect('category_detail', category_id=category_id)

    else:
        subcategory_form = SubcategoryForm()

    context = {
        'category': category,
        'subcategories': subcategories,
        'subcategory_form': subcategory_form,
    }
    return render(request, 'inventory/category_detail.html', context)



@login_required
def update_subcategory(request, category_id, subcategory_id):
    category = get_object_or_404(Category, id=category_id)
    subcategory = get_object_or_404(Subcategory, id=subcategory_id, category=category)

    if request.method == 'POST':
        form = SubcategoryForm(request.POST, instance=subcategory)
        if form.is_valid():
            form.save()
            return redirect('category_detail', category_id=category_id)
    else:
        form = SubcategoryForm(instance=subcategory)

    context = {
        'category': category,
        'subcategory': subcategory,
        'form': form,
    }

    return render(request, 'update_subcategory.html', context)

# View to delete subcategory
@login_required
def delete_subcategory(request, category_id, subcategory_id):
    category = get_object_or_404(Category, id=category_id)
    subcategory = get_object_or_404(Subcategory, id=subcategory_id, category=category)

    if request.method == 'POST':
        subcategory.delete()
        return redirect('category_detail', category_id=category_id)

    context = {
        'category': category,
        'subcategory': subcategory,
    }

    return render(request, 'delete_subcategory.html', context)


# View to add items to their respective sub categories
@login_required
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.subcategory_id = request.POST.get('subcategory_id')
            item.save()
            return redirect('inventory_items')
    else:
        form = ItemForm()

    context = {
        'form': form,
    }

    return render(request, 'inventory/category_detail.html', context)

@login_required
def inventory_items(request):
    subcategories = Subcategory.objects.all()
    items = Item.objects.all()
    context = {
        'items': items,
        'subcategories': subcategories
    }
    return render(request, 'inventory/items.html', context)

@login_required
def get_items_by_subcategory(request, subcategory_id):
    subcategory = get_object_or_404(Subcategory, id=subcategory_id)
    items = Item.objects.filter(subcategory=subcategory)
    data = {
        'items': [
            {
                'name': item.name,
                'price': item.price,
                'image': item.image.url,
                'in_stock': item.in_stock,
            }
            for item in items
        ]
    }
    return JsonResponse(data)


@login_required
def view_subcategory(request, category_id, subcategory_id):
    category = get_object_or_404(Category, id=category_id)
    subcategory = get_object_or_404(Subcategory, id=subcategory_id)
    items = Item.objects.filter(subcategory=subcategory)

    context = {
        'category': category,
        'subcategory': subcategory,
        'items': items
    }

    return render(request, 'inventory/view_subcategory.html', context)


def selling_point(request):
    categories_with_items = Category.objects.prefetch_related('subcategory_set__item_set').all()
    return render(request, 'sales/selling_point.html', {'categories_with_items': categories_with_items})

def checkout(request):
    if request.method == 'POST':
        try:
            data = request.POST
            cart_items = data.get('cartItems')  # Assuming 'cartItems' is a JSON string representation of the cart items list
            total_price = data.get('totalPrice')

            # Process the checkout, update the database, etc.
            # You can access individual cart items and total price in 'cart_items' and 'total_price' variables

            # Return a JSON response indicating success or failure
            return JsonResponse({'message': 'Checkout successful!'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)



def add_to_cart(request, item_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        item = Item.objects.get(pk=item_id)

        if not item.in_stock or item.quantity < quantity:
            return redirect('selling_point')

        user_cart, created = Cart.objects.get_or_create(user=request.user)

        cart_item, created = CartItem.objects.get_or_create(cart=user_cart, item=item)
        cart_item.quantity += quantity
        cart_item.save()

        item.quantity -= quantity
        item.save()

    return redirect('selling_point')


@login_required
def remove_from_cart(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        cart_item = get_object_or_404(CartItem, id=item_id)
        cart_item.delete()

    return redirect('selling_point')

@login_required
def generate_receipt(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.cartitem_set.all()
    total_amount = sum(item.item.price * item.quantity for item in cart_items)

    return render(request, 'sales/receipt.html', {'cart_items': cart_items, 'total_amount': total_amount})
