document.addEventListener('DOMContentLoaded', () => {
    const cartItemsElement = document.getElementById('cartItems');
    const totalPriceElement = document.getElementById('totalPrice');
    const addToCartForms = document.querySelectorAll('[data-item-id]');
    const checkoutBtn = document.getElementById('checkoutBtn');

    const items = categoriesWithItems.flatMap(category => category.subcategory_set.flatMap(subcategory => subcategory.item_set));

    const cartItems = [];

    addToCartForms.forEach((form) => {
        form.addEventListener('submit', addToCart);
    });

    function addToCart(event) {
        event.preventDefault();
        const form = event.target;
        const itemId = form.getAttribute('data-item-id');
        const quantity = form.elements['quantity'].valueAsNumber;
        const item = items.find((item) => item.pk === parseInt(itemId));
        if (!item) return;

        const existingCartItem = cartItems.find((cartItem) => cartItem.id === itemId);

        if (existingCartItem) {
            existingCartItem.quantity += quantity;
        } else {
            cartItems.push({ ...item, id: itemId, quantity });
        }

        updateCart();
    }

    function updateCart() {
        cartItemsElement.innerHTML = '';
        let total = 0;

        cartItems.forEach((cartItem) => {
            const { id, name, price, quantity } = cartItem;
            const totalPrice = price * quantity;
            total += totalPrice;

            const li = document.createElement('li');
            li.textContent = `${name} - ${quantity} x KES ${price.toFixed(2)} = KES ${totalPrice.toFixed(2)}`;
            cartItemsElement.appendChild(li);
        });

        totalPriceElement.textContent = `KES ${total.toFixed(2)}`;
    }

    checkoutBtn.addEventListener('click', processCheckout);

    function processCheckout() {
        const data = {
            cartItems: cartItems,
            totalPrice: totalPriceElement.textContent
        };

        fetch('/checkout/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            alert('Checkout successful!');
            clearCart();
        })
        .catch(error => {
            console.error('Error during checkout:', error);
            alert('Checkout failed. Please try again.');
        });
    }

    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }

    function clearCart() {
        cartItems.length = 0;
        updateCart();
    }

    function clearSearch() {
        itemSearchInput.value = '';
        filterItems();
    }

    // Function filterItems() remains the same as in the previous answer
    // Function clearSearch() remains the same as in the previous answer
    // Function updateCart() remains the same as in the previous answer

    updateCart();
});
