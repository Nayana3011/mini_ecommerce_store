from django.urls import path

from .api_views import OrderListAPIView, OrderDetailAPIView, CancelOrderAPIView


urlpatterns = [

    path(
        'orders/',
        OrderListAPIView.as_view()
    ),
    
    path(
        'orders/<int:pk>/',
        OrderDetailAPIView.as_view(),
        name='api_order_detail'
    ),
    
    path(
        'orders/<int:pk>/cancel/',
        CancelOrderAPIView.as_view()
    ),


]