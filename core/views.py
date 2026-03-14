from django.shortcuts import render
from django.db import transaction
# from django.core.cache import cache

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import StoreSerializer
from .models import Store

from rest_framework.exceptions import NotFound
# store = cache.get('store_list_master')
        # if store is None:
        #     store = Store.objects.all()
        #     cache.set('store_list_master', store, timeout=5 * 60)

class StoreView(APIView):
    def get(self, request):
        store = Store.objects.all()
        serializer = StoreSerializer(store, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = StoreSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            with transaction.atomic():
                serializer.save()
                # cache.delete('store_list_master')
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StoreDetailView(APIView):
    def get_by_key(self, key):
        try:
            return Store.objects.get(key=key)
        except Store.DoesNotExist as e:
            raise NotFound(detail="Store entry not found")

    def get(self, request, key):
        store = self.get_by_key(key)
        
        serializer = StoreSerializer(store)
        return Response(serializer.data)
    
    def put(self, request, key):
        store = self.get_by_key(key)
        serializer = StoreSerializer(store, data=request.data, partial=True)
        if serializer.is_valid():
            with transaction.atomic():
                serializer.save()
                return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, key):
        store = self.get_by_key(key)

        store.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  
    

def read_primary(request):
    data = Store.objects.using('default').all()  # Primary DB
    return Response({"primary_data": data})

def read_replica(request):
    data = Store.objects.using('replica').all()  # Primary DB
    return Response({"replica": data})



