from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from store import serializers
from store.models import *
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication

class ProductReviewAddView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)

    def post(self, request, id):
        """ Add review for the product """
        product = Product.objects.get(id=id)
        user = request.user

        if Review.objects.filter(product=product, user=user).exists():
            return Response(
                {"detail": "You have already reviewed this product."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        rating = request.data.get('rating')
        
        if not rating:
            return Response(
                {"detail": "Rating is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        comment = request.data.get('comment')
        Review.objects.create(product=product, user=user, rating=rating, comment=comment)
        return Response({"message": "review is created successfully"}, status=status.HTTP_201_CREATED)

class ProductReviewGetView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, id):
        reviews = Review.objects.filter(product_id=id)
        return Response(serializers.ReviewSerializer(reviews, many=True).data, status=status.HTTP_200_OK)

class ReviewDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)

    def put(self, request, id):
        """ Update comment of the product (required id of the review) """
        review = get_object_or_404(Review, id=id)
        if review.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = serializers.ReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Review updated successfully.", "data": serializer.data},
                status=status.HTTP_200_OK
            )
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        review = get_object_or_404(Review, id=id)
        if review.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        review.delete()
        return Response({"message": "Review deleted"}, status=status.HTTP_204_NO_CONTENT)
    
    def get(self, request, id):
        review = get_object_or_404(Review, id=id)
        if review.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = serializers.ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
