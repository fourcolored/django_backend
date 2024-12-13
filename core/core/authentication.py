from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from users.models import CustomUser as User 

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get('Authorization')
        
        if token is None:
            # Check if token is provided in cookies
            token = request.COOKIES.get('access_token')
        
        if not token:
            return None

        try:
            access_token = AccessToken(token)

            user_id = access_token.payload.get('user_id')
            user = User.objects.get(id=user_id)

        except (Exception, InvalidToken) as e:
            raise AuthenticationFailed('Invalid token or expired token')

        return (user, access_token)
