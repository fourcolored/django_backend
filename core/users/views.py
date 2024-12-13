from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from users import serializers
from store.models import ShoppingCart, WishList

class RegisterView(APIView):
    """
    {
        "username": "user",
        "email": "example@example.com",
        "password1": "p4ssword123",
        "password2": "p4ssword123"
    }

    """
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = serializers.RegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            ShoppingCart.objects.create(user=user)
            WishList.objects.create(user=user)
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        
        return Response({"message": "Error unable to register"},status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        return Response({"message": "Provide POST data to register a user."}, status=status.HTTP_200_OK)
        

class LoginView(APIView):
    """
    {
        "username":"user",
        "password":"p4ssword123"
    }
    """
    permission_classes = (AllowAny, )

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(
            username=username, password=password)
        if user is None:
            return Response({"Error": "User is None"}, status=status.HTTP_401_UNAUTHORIZED)
        
        login(request, user)

        return Response({"message": "User logged in successfully"}, status=status.HTTP_200_OK)
    
    def get(self, request):
        response = Response({"message": "Provide POST data to login"})
        return response

def logout_view(request):
    logout(request)
    # response = Response({"message": "User logged out successfully"}, status=status.HTTP_200_OK)
    response = redirect('users:login')
    # response.delete_cookie('jwt_token')
    # response.delete_cookie('temp_user_id')
    return response

