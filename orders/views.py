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
from django.http import JsonResponse


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

                variant = ProductVariant.objects.select_for_update().get(id=item['variant'].id)

                if variant.stock_quantity < item['quantity']:
                    raise ValueError("Not enough stock available")

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

    return render(request,'orders/checkout.html')
    

@login_required
def order_history(request):

    orders = Order.objects.filter(buyer=request.user)

    return render(request,'orders/history.html',
        {
            'orders': orders
        }
    )

@login_required    
def order_detail(request, order_id):

    order = get_object_or_404(Order,id=order_id,buyer=request.user)

    items = OrderItem.objects.filter(order=order)

    return render(request,'orders/detail.html',
        {
            'order': order,
            'items': items
        }
    )

@login_required    
def mock_payment(request, order_id):

    order = get_object_or_404(Order,id=order_id,buyer=request.user)

    order.status = 'paid'
    order.save()

    send_order_confirmation.delay(order.id)
    
    return render(request,'orders/payment_success.html',{'order': order})


@login_required
def payment_page(request, order_id):

    order = get_object_or_404(Order,id=order_id,buyer=request.user)

    if request.method == "POST":

        card_number = request.POST.get("card_number").replace(" ", "")

        if card_number == "4242424242424242":

            order.status = "paid"
            order.save()

            send_order_confirmation.delay(order.id)

            return render(request,"orders/payment_success.html",
                {"order": order}
            )

        else:

            return render(request,"orders/payment_failed.html")

    return render(request,"orders/payment_page.html",
        {"order": order}
    )


def stripe_test(request):

    session = stripe.checkout.Session.create(
        success_url="http://localhost:8000/",
        cancel_url="http://localhost:8000/",
        payment_method_types=["card"],
        mode="payment",
        line_items=[]
    )

    return JsonResponse(
        {"session": str(session)}
    )
