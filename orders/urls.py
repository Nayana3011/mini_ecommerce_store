from django.urls import path
from . import views

urlpatterns = [

    path('checkout/',views.checkout,name='checkout'),

    path('',views.order_history,name='order_history'),
    
    path('<int:order_id>/',views.order_detail,name='order_detail'),

    path('payment/<int:order_id>/',views.mock_payment,name='mock_payment'),
    
    path('stripe-test/',views.stripe_test,name='stripe_test'),
    
    path('pay/<int:order_id>/',views.payment_page,name='payment_page'),

]