from django.db import models
from django.contrib.auth.models import User
from catalogue.models import ProductVariant


class Order(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
        ('cancelled', 'Cancelled'),
    ]

    buyer = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    shipping_address = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return f"Order {self.id}"


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE
    )

    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField()

    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.variant.sku}"
