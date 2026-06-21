from celery import shared_task

from django.core.mail import EmailMultiAlternatives

from .models import Order
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_order_confirmation(order_id):

    try:
        order = Order.objects.get(id=order_id)

        html_content = f"""
        <h2>Order Confirmation</h2>

        <p>Order ID: {order.id}</p>

        <table border="1" cellpadding="5">

            <tr>
                <th>Product</th>
                <th>Quantity</th>
                <th>Price</th>
            </tr>
        """

        for item in order.orderitem_set.all():

            html_content += f"""
            <tr>
                <td>{item.variant}</td>
                <td>{item.quantity}</td>
                <td>{item.unit_price}</td>
            </tr>
            """

        html_content += f"""
        </table>

        <p>Total: {order.total}</p>
        """

        email = EmailMultiAlternatives(
            subject=f"Order #{order.id} Confirmation",
            body="Your order has been placed successfully.",
            from_email="store@example.com",
            to=[order.buyer.email]
        )

        email.attach_alternative(
            html_content,
            "text/html"
        )

        email.send()

        return True
    
    except Exception as e:

        logger.error(
            f"Order confirmation failed: {e}"
        )

        return False