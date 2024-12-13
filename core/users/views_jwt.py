from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        refresh = response.data.get('refresh')
        access = response.data.get('access')

        response.set_cookie(
            key='access_token', 
            value=access, 
            httponly=True, 
            secure=True,
            max_age=60*60,
        )
        response.set_cookie(
            key='refresh_token', 
            value=refresh, 
            httponly=True, 
            secure=60*60,
        )

        return response
