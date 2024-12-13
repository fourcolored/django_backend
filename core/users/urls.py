from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from store.views import *
from users.views import *
from users.views_jwt import *

app_name = 'users'
urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),    
    path('register/', RegisterView.as_view(), name='login'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
]