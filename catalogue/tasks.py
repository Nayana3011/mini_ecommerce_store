from celery import shared_task
from django.core.mail import send_mail

from .models import ProductVariant


@shared_task
def low_stock_alert():

    low_stock_items = ProductVariant.objects.filter(
        stock_quantity__lt=5
    )

    if not low_stock_items.exists():
        return "No low stock items"

    message = ""

    for item in low_stock_items:

        message += (
            f"SKU: {item.sku}\n"
            f"Stock: {item.stock_quantity}\n\n"
        )

    send_mail(
        subject="Low Stock Alert",
        message=message,
        from_email="store@example.com",
        recipient_list=["seller@example.com"],
        fail_silently=False,
    )

    return "Low stock email sent"