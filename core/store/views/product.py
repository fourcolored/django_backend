from django.core.cache import cache
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny, IsAuthenticated

from store import serializers
from store.models import *

product_timeout = 60 * 5

class CategoryView(APIView):
    """
    Create category
    Get category list
    """
    permission_classes = (AllowAny,)
    def post(self, request):
        """
        Without parent:
        {
            "name": "Electronics"
        }
        
        With parent:
        {
            "name": "Mobile Phones",
            "parent": 1
        }
        """
        serializer = serializers.CategorySerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request):
        cateogries = Category.objects.all()
        serializer = serializers.CategorySerializer(cateogries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CategoryDetailView(APIView):
    permission_classes = (AllowAny,)
    def get_object(self, id):
        try:
            category = Category.objects.get(pk=id)
            return category
        except Category.DoesNotExist as e:
            raise NotFound(detail="Categorogy not found", code=status.HTTP_404_NOT_FOUND)
    
    def get(self, request, id):
        """
        Get cateogry details with associated products
        """
        instance = self.get_object(id)
        cat_serializer = serializers.CategorySerializer(instance)
        return Response(cat_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        """
        Delete category
        """
        instance = self.get_object(id)
        instance.delete()
        return Response({"message": f"category with id {id} is deleted"}, status=status.HTTP_204_NO_CONTENT)

class ProductView(APIView):
    """
    Create product
    Get list of products
    """
    permission_classes = (AllowAny,)
    def post(self, request):
        if cache.get("products"):
            cache.delete("products")
        serializer = serializers.ProductSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request):
        products = cache.get("products")
        if not products:
            product_instances = Product.objects.all()
            products = serializers.ProductSerializer(product_instances, many=True)
            cache.set("products", products, timeout=5*60)

        return Response(products.data, status=status.HTTP_200_OK)

class ProductDetailView(APIView):
    permission_classes = (AllowAny,)
    def get_object(self, id):
        try:
            product = Product.objects.get(pk=id)
            return product
        except Product.DoesNotExist as e:
            raise NotFound(detail="Product not found", code=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, id):
        """
        Change name, description, price, stock_quantity
        """
        instance = cache.get(f"product_{id}")
        if not instance:
            instance = self.get_object(id)

        serializer = serializers.ProductSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            instance = serializer.save()
            cache.set(f"product_{id}", instance, timeout=product_timeout)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        """
        Get product details [with reviews]
        """
        instance = cache.get(f"product_{id}")
        if not instance:
            instance = self.get_object(id)
            cache.set(f"product_{id}", instance, timeout=product_timeout)

        product_serializer = serializers.ProductSerializer(instance)
        
        return Response({
            "product": product_serializer.data
        }, status=status.HTTP_200_OK)
    
    def delete(self, request, id):
        """
        Delete product
        """
        instance = cache.get(f"product_{id}")
        if not instance:
            instance = self.get_object(id)
        else:
            cache.delete(f"product_{id}")

        instance.delete()
        return Response({"message": f"product with id {id} is deleted"}, status=status.HTTP_204_NO_CONTENT)