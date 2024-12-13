from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from store import serializers
from store.models import *
from rest_framework_simplejwt.authentication import JWTAuthentication

class WishListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)
    def get_object(self, user):
        wishlist, _ = WishList.objects.get_or_create(user=user)
        return wishlist

    def post(self, request):
        """ user adds product to wishlist """
        product_id = request.data.get('product_id')
        if not product_id:
            return Response(
                {"error": "Product ID is required."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        product = get_object_or_404(Product, id=product_id)

        wishlist = self.get_object(request.user)
        
        _, created = WishListItem.objects.get_or_create(wishlist=wishlist, product=product)
        
        if created:
            return Response(
                {"message": "Product added to wishlist successfully."}, 
                status=status.HTTP_201_CREATED
            )
        return Response(
                {"message": "Product is already in the wishlist."}, 
                status=status.HTTP_200_OK
            )

    def get(self, request):
        """ Get wishlist items """

        wishlist = self.get_object(request.user)
        items = WishListItem.objects.filter(wishlist=wishlist)
        # items = WishListItem.objects.select_related('product').filter(wishlist=wishlist)

        serializer = serializers.WishListSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class WishListItemView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)
    
    def get_object(self, user):
        wishlist, _ = WishList.objects.get_or_create(user=user)
        return wishlist
    
    def delete(self, request, id):
        """ Remove item from wishlist by product id """
        try:
            wishlist = WishListItem.objects.get(product_id=id, wishlist=self.get_object(request.user))
            wishlist.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except WishListItem.DoesNotExist:
            return Response({"error": "Product not found in wishlist."}, status=status.HTTP_404_NOT_FOUND)
    

