from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework_simplejwt.authentication import JWTAuthentication
from store import serializers
from store.models import *
import logging

logger = logging.getLogger('django')

class ShoppingCartView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)

    def get_object(self, user):
        cart, _ = ShoppingCart.objects.get_or_create(user=user)
        return cart

    def post(self, request):
        """ Create CartItem ( add product to shopping cart ) """

        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1) # not required

        product = get_object_or_404(Product, id=product_id)

        cart = self.get_object(request.user)

        _, created = CartItem.objects.get_or_create(cart_id=cart.id, product=product, quantity=quantity)
        
        if created:
            return Response(
                {"message": "Product added to shopping cart successfully."}, status=status.HTTP_201_CREATED
            )
        return Response(
                {"message": "Product is already in the shopping cart."}, 
                status=status.HTTP_200_OK
            ) 
    
    def get(self, request):
        """ Get items in shopping cart """
        # instance = self.get_object(request.user)
        # items = instance.items.all()
        # print("SHOPPING_CART_VIEW", self.get_object(request.user))
        logger.debug("SHOPPING_CART_VIEW: %s", self.get_object(request.user), request.user)
        cart_items = CartItem.objects.select_related('product').filter(cart=self.get_object(request.user))
        serializer = serializers.CartItemSerializer(cart_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # def delete(self, request):
    #     """ Remove cart item by product_id in shopping cart """
    #     try:
    #         product_id = request.data.get("product_id")
    #         if not product_id:
    #             return Response({"error": "Product ID is required."}, status=status.HTTP_400_BAD_REQUEST)
    #         cart_item = CartItem.objects.get(product_id=product_id, cart=self.get_object(request.user))
    #         cart_item.delete()
    #         return Response(status=status.HTTP_204_NO_CONTENT)
    #     except CartItem.DoesNotExist:
    #         return Response({"error": "Product not found in shopping cart."}, status=status.HTTP_404_NOT_FOUND)

class ShoppingCartDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    
    permission_classes = (IsAuthenticated,)

    def get_object(self, id, user):
        try:
            cart_item = CartItem.objects.get(id=id)
            if user != cart_item.cart.user:
                raise PermissionDenied("You do not have permission to access this cart item.")
            return cart_item
        except CartItem.DoesNotExist as e:
             raise NotFound("Cart Item not found.")
        
    def get(self, request, id):
        """
        get items detail
        """
        try:
            instance = self.get_object(id, request.user)
            serializer = serializers.CartItemSerializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except NotFound as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
    
    def put(self, request, id):
        """
        change quantity of the item in shopping cart
        """
        try:
            instance = self.get_object(id, request.user)
            instance.quantity = request.data.get('quantity')
            instance.save()
            return Response({"message": "Updated successfully"}, status=status.HTTP_200_OK)
        except NotFound as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
    
    def delete(self, request, id):
        """
        delete item from shopping cart
        """
        try:
            instance = self.get_object(id, request.user)
            instance.delete()
            return Response({"message": "Deleted item"}, status=status.HTTP_204_NO_CONTENT)
        except NotFound as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)