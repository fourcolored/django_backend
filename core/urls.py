from django.urls import path
# from rest_framework.routers import DefaultRouter
from .views import StoreView, StoreDetailView, read_primary, read_replica


urlpatterns = [
    path('', StoreView.as_view()),
    path('<str:key>/', StoreDetailView.as_view()),
    path('read_primary/', read_primary, name='read_primary'),
    path('read_replica/', read_replica, name='read_replica'),
]