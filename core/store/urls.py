from django.urls import path
from store.views import *

urlpatterns = [
    path('categories/', CategoryView.as_view(), name='category_endpoint'),
    path('categories/<int:id>/', CategoryDetailView.as_view(), name='category_details_endpoint'),

    path('products/', ProductView.as_view(), name='product_endpoint'),
    path('products/<int:id>/', ProductDetailView.as_view(), name='product_details_endpoint'),
    
    path('products/<int:id>/review/', ProductReviewAddView.as_view(), name='review_endpoint'),
    path('products/<int:id>/reviews/', ProductReviewGetView.as_view(), name='review_endpoint'),
    path('review/<int:id>/', ReviewDetailView.as_view(), name='review_details_endpoint'),
    
    path('shopping_cart/', ShoppingCartView.as_view(), name='shopping_cart_endpoint'),
    path('shopping_cart/<int:id>/', ShoppingCartDetailView.as_view(), name='shopping_cart_details_endpoint'),

    path('orders/', OrderView.as_view(), name='order_endpoint'),
    path('orders/<int:id>/', OrderDetailView.as_view(), name='order_details_endpoint'),
    # path('orders/<int:id>/payment/', PaymentConfirmView.as_view(), name='payment_endpoint'),

    path('wishlist/', WishListView.as_view(), name='wishlist_endpoint'),
    path('wishlist/<int:id>/', WishListItemView.as_view(), name='remove_product_from_wishlist_endpoint'),
]