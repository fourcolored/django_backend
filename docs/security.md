# Security in High-Load Systems
Security is main aspect of the system to protect sensitve user data and other information. A secure system ensures confidentiality, integrity, and security of data, preventing unauthorized access.

## JWT Authentication
Jwt authentication is setup using `rest_framework_simplejwt`.
```
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}
```
Configuration of jwt tokens: tokens lifetimes and update_last_login ensures that user's last login time updated whenever user autenticate.
```
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
    "UPDATE_LAST_LOGIN": True,
    'SLIDING_TOKEN_LIFETIME': timedelta(days=30),
    'SLIDING_TOKEN_REFRESH_LIFETIME_LATE_USER': timedelta(days=1),
    'SLIDING_TOKEN_LIFETIME_LATE_USER': timedelta(days=30),
}
```

## Registration
User registration is handled via an APIView where user data is validated using RegisterSerializer and uses the AllowAny permission, meaning anyone can access it and register a new user.
```
class RegisterView(APIView):

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
``` 
## Login      
The login view uses Django’s authenticate method to verify the user’s credentials.
```
class LoginView(APIView):

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
```

## Security Middleware
```
class SecurityMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['Content-Security-Policy'] = "default-src 'self'"
        return response
```
- X-Content-Type-Options: 'nosniff' is  tells the browser not to try guessing the file type.
- X-Frame-Options: This header prevents your web pages from being shown inside iframes on other websites. This protects against clickjacking.
- Content-Security-Policy: This header controls where the browser is allowed to load resources from. By restricting resources to come only from your own website ('self'), it helps block attacks like cross-site scripting (XSS), where an attacker tries to inject harmful code into your site. 