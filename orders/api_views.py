from rest_framework import generics

from .models import Order
from .serializers import OrderSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404
from django.utils import timezone

from datetime import timedelta


class OrderListAPIView(generics.ListAPIView):

    serializer_class = OrderSerializer

    def get_queryset(self):

        queryset = Order.objects.filter(buyer=self.request.user).order_by('-created_at')
        status = self.request.GET.get('status')

        if status:
            queryset = queryset.filter(status=status)

        return queryset
        
        
class OrderDetailAPIView(generics.RetrieveAPIView):

    serializer_class = OrderSerializer

    permission_classes = [IsAuthenticated]

    def get_object(self):

        return get_object_or_404(
            Order,
            id=self.kwargs['pk'],
            buyer=self.request.user
        )
        
        
class CancelOrderAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self,request,pk):

        order = get_object_or_404(Order,id=pk,buyer=request.user)

        if order.status != 'pending':

            return Response(
                {
                    'error':'Only pending orders can be cancelled'
                },
                status=403
            )

        if timezone.now() - order.created_at > timedelta(hours=24):

            return Response(
                {
                    'error':'Cancellation period expired'
                },
                status=403
            )

        order.status = 'cancelled'

        order.save()

        return Response(
            {
                'message':'Order cancelled successfully'
            }
        )