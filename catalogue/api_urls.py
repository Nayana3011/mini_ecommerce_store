from django.urls import path
from .api_views import (ProductListAPIView, ProductDetailAPIView, ReviewCreateAPIView)

urlpatterns = [

    path(
        'products/',
        ProductListAPIView.as_view()
    ),

    path(
        'products/<slug:slug>/',
        ProductDetailAPIView.as_view()
    ),
    
    path(
    'reviews/',
    ReviewCreateAPIView.as_view(),
    name='review_create'
    ),

]