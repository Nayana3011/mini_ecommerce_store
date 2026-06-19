from django.shortcuts import render, redirect
from catalogue.models import ProductVariant
from .cart import Cart


def cart_detail(request):

    cart = Cart(request)

    return render(
        request,
        'cart/detail.html',
        {
            'cart': cart,
            'cart_count': len(cart)
        }
    )


def cart_add(request, variant_id):

    cart = Cart(request)

    variant = ProductVariant.objects.get(
        id=variant_id
    )

    cart.add(variant)

    return redirect('cart_detail')


