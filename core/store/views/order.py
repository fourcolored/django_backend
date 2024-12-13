from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework_simplejwt.authentication import JWTAuthentication
from store import serializers
from store.models import *
from store.tasks import sending_order_confirmation_email, processing_payment

class OrderView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """ Create order """
        cart = ShoppingCart.objects.get(user=request.user)
        if not cart.items.exists():
            return Response({"Error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(user=request.user)
        # cart_items = cart.items.all()
        cart_items = CartItem.objects.select_related('product').filter(cart=cart)

        total_price = 0
        orders = []
        for item in cart_items:
            order_item = OrderItem(order=order, product=item.product, quantity=item.quantity, price=item.product.price)
            orders.append(order_item)
            
            total_price += item.product.price * item.quantity
        
        OrderItem.objects.bulk_create(orders)
        
        order.total_amount = total_price
        order.save()

        payment = Payment.objects.create(
            order=order, 
            payment_method="credit_card",
            status='PENDING',
            amount=total_price
        )

        processing_payment.delay(payment.id)
        sending_order_confirmation_email.delay(order.id, request.user.email)

        return Response({"message": "order is created successfully"}, status=status.HTTP_201_CREATED)

    def get(self, request):
        """
        Get order list
        """
        orders = request.user.orders.all()
        # orders = Order.objects.select_related('user').prefetch_related('items', 'payment').filter(user=request.user)
        serializer = serializers.OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class OrderDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)

    def get_object(self, id, user):
        try:
            order = Order.objects.get(id=id)
            if user != order.user:
                raise PermissionDenied("You do not have permission to access this order.")
            return order
        except Order.DoesNotExist as e:
            raise NotFound("Order not found.")
        
    def get(self, request, id):
        """ Get order details """
        try:
            instance = self.get_object(id, request.user)
            serializer = serializers.OrderSerializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except NotFound as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
    
    def put(self, request, id):
        """ Cancel the order """
        try:
            instance = self.get_object(id, request.user)
            if instance.order_status == "COMPLETED":
                return Response ({"message": "Order can't be cancelled & payment already verified"}, status=status.HTTP_200_OK)
            instance.order_status = 'CANCELLED'
            instance.save()
            serializer = serializers.OrderSerializer(instance)
            return Response({
                "message": "Order status has been changed",
                "order": serializer.data
            }, status=status.HTTP_200_OK)
        except NotFound as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)