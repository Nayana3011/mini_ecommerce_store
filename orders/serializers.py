from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):

    product = serializers.CharField(source='variant.product.name')

    class Meta:

        model = OrderItem

        fields = [
            'product',
            'quantity',
            'unit_price'
        ]


class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(
        source='orderitem_set',
        many=True,
        read_only=True
    )

    class Meta:

        model = Order

        fields = [
            'id',
            'status',
            'shipping_address',
            'total',
            'created_at',
            'items'
        ]