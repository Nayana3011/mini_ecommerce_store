from rest_framework import generics

from .models import Product
from .serializers import ProductSerializer

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Review
from .api_serializers import ReviewSerializer

from rest_framework.exceptions import ValidationError


class ProductListAPIView(generics.ListAPIView):

    serializer_class = ProductSerializer

    def get_queryset(self):

        queryset = Product.objects.filter(is_active=True).order_by('id')

        category = self.request.GET.get('category')

        if category:

            queryset = queryset.filter(category__name=category)

        min_price = self.request.GET.get('min_price')

        max_price = self.request.GET.get('max_price')

        if min_price:

            queryset = queryset.filter(productvariant__price__gte=min_price)

        if max_price:

            queryset = queryset.filter(productvariant__price__lte=max_price)

        in_stock = self.request.GET.get('in_stock')

        if in_stock == 'true':

            queryset = queryset.filter(productvariant__stock_quantity__gt=0)

        return queryset.distinct()


class ProductDetailAPIView(generics.RetrieveAPIView):
    
    queryset = Product.objects.filter(
        is_active=True
    )

    serializer_class = ProductSerializer

    lookup_field = 'slug'
    
    
class ReviewCreateAPIView(generics.CreateAPIView):
    
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    permission_classes = [IsAuthenticated]

    def perform_create(self,serializer):

        product = serializer.validated_data['product']

        if Review.objects.filter(product=product,buyer=self.request.user).exists():

            raise ValidationError("You already reviewed this product.")

        serializer.save(buyer=self.request.user)