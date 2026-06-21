from django.shortcuts import render
from .models import Product
from django.contrib.auth.decorators import login_required

@login_required
def product_list(request):

    products = Product.objects.filter(is_active=True)

    return render(
        request,
        'catalogue/product_list.html',
        {
            'products': products
        }
    )