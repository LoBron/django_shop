from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .cart import Cart
from .forms import CartAddProductForm
from catalog.models import Product


@require_POST
def cart_add(request, prod_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=prod_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect(request.META.get('HTTP_REFERER'))


def cart_remove(request, prod_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=prod_id)
    cart.remove(product)
    return redirect('cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
                                                                   'update': True})
    return render(request, 'cart/cart_detail.html', {'cart': cart})

def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect('catalog_home')