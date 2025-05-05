from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from store.models import Product
from .cart import Cart
from .models import SavedCart, SavedCartItem
from .forms import CartAddProductForm

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])
        
        # If AJAX request, return JSON response
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'message': f'{product.name} added to cart',
                'cart_total': len(cart),
                'cart_total_price': float(cart.get_total_price()),
            })

    return redirect('cart:cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    
    # If AJAX request, return JSON response
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'message': f'{product.name} removed from cart',
            'cart_total': len(cart),
            'cart_total_price': float(cart.get_total_price()),
        })
    
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'override': True})
    
    # If AJAX request, return JSON response with cart data
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart_items = []
        for item in cart:
            cart_items.append({
                'id': item['product'].id,
                'name': item['product'].name,
                'price': float(item['price']),
                'quantity': item['quantity'],
                'total_price': float(item['total_price']),
                'image_url': item['product'].image.url if item['product'].image else None,
                'product_url': item['product'].get_absolute_url(),
            })
        
        return JsonResponse({
            'cart_items': cart_items,
            'cart_total': len(cart),
            'cart_total_price': float(cart.get_total_price()),
        })
    
    return render(request, 'cart/detail.html', {'cart': cart})

@login_required
def save_cart_for_later(request):
    """Save current cart items to user's saved cart"""
    cart = Cart(request)
    if len(cart) > 0:
        saved_cart = SavedCart.objects.create(user=request.user)
        for item in cart:
            SavedCartItem.objects.create(
                saved_cart=saved_cart,
                product=item['product'],
                quantity=item['quantity']
            )
        cart.clear()  # Clear the session cart after saving
        
        # If AJAX request, return JSON response
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'message': 'Cart saved successfully',
                'redirect_url': request.build_absolute_uri('/cart/'),
            })
        
        return redirect('cart:cart_detail')
    
    # If AJAX request with empty cart
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'error',
            'message': 'Cannot save empty cart',
        })
    
    return redirect('store:product_list')

@login_required
def view_saved_carts(request):
    """View all saved carts for the current user"""
    saved_carts = SavedCart.objects.filter(user=request.user)
    return render(request, 'cart/saved_carts.html', {'saved_carts': saved_carts})

@login_required
def load_saved_cart(request, cart_id):
    """Load a saved cart into the current session cart"""
    saved_cart = get_object_or_404(SavedCart, id=cart_id, user=request.user)
    cart = Cart(request)
    cart.clear()  # Clear current cart first
    
    for item in saved_cart.items.all():
        cart.add(product=item.product, quantity=item.quantity)
    
    # If AJAX request, return JSON response
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'message': 'Saved cart loaded successfully',
            'redirect_url': request.build_absolute_uri('/cart/'),
        })
    
    return redirect('cart:cart_detail')

@login_required
def delete_saved_cart(request, cart_id):
    """Delete a saved cart"""
    saved_cart = get_object_or_404(SavedCart, id=cart_id, user=request.user)
    saved_cart.delete()
    
    # If AJAX request, return JSON response
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'message': 'Saved cart deleted successfully',
        })
    
    return redirect('cart:view_saved_carts')
