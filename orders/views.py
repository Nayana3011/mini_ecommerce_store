from django.shortcuts import render, redirect
from .models import Order, OrderItem
from cart.cart import Cart
from django.shortcuts import get_object_or_404
from django.db import transaction
from catalogue.models import ProductVariant
import stripe
from django.conf import settings
from .tasks import send_order_confirmation
from django.contrib.auth.decorators import login_required


stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def checkout(request):

    cart = Cart(request)

    if request.method == "POST":

        with transaction.atomic():

            order = Order.objects.create(
                buyer=request.user,
                shipping_address=request.POST['address']
            )

            total = 0

            for item in cart:

                variant = ProductVariant.objects.select_for_update().get(
                    id=item['variant'].id
                )

                if variant.stock_quantity < item['quantity']:
                    raise ValueError(
                        "Not enough stock available"
                    )

                variant.stock_quantity -= item['quantity']
                variant.save()

                OrderItem.objects.create(
                    order=order,
                    variant=variant,
                    quantity=item['quantity'],
                    unit_price=variant.price
                )

                total += item['total_price']

            order.total = total
            order.save()

            cart.clear()

        return redirect('order_history')

    return render(
        request,
        'orders/checkout.html'
    )
    

@login_required
def order_history(request):

    orders = Order.objects.filter(
        buyer=request.user
    )

    return render(
        request,
        'orders/history.html',
        {
            'orders': orders
        }
    )

@login_required    
def order_detail(request, order_id):

    order = get_object_or_404(
    Order,
    id=order_id,
    buyer=request.user
    )

    items = OrderItem.objects.filter(
        order=order
    )

    return render(
        request,
        'orders/detail.html',
        {
            'order': order,
            'items': items
        }
    )

@login_required    
def mock_payment(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        buyer=request.user
    )

    order.status = 'paid'
    order.save()

    send_order_confirmation.delay(order.id)
    
    return render(request,'orders/payment_success.html',{'order': order})

