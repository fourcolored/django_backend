from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import NotFound, PermissionDenied
from store import serializers
from store.models import *
from store.tasks import processing_payment

class PaymentConfirmView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, id):
        """ Confirm payment """
        
        order = get_object_or_404(Order, id=id)

        if order.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        try:
            payment = Payment.objects.get(order=order)
        except Payment.DoesNotExist:
            order.order_status = 'CANCELLED'
            order.save()
            return Response({"detail": "Payment for this order does not exist."}, status=status.HTTP_404_NOT_FOUND)
            
        if order.order_status == 'CANCELLED':
            payment.delete()
            return Response({"message": "Payment deleted"}, status=status.HTTP_204_NO_CONTENT)
        
        processing_payment.delay(payment.id)

        return Response({"message": "Payment confirmed"}, status=status.HTTP_200_OK)