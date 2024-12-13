from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.test import APIClient
from users.models import CustomUser
from store.models import *

class OrderProcessingTest(APITestCase):
    def setUp(self):
        username = 'testuser'
        password = 'p4ssword123'
        email = "testuser@mail.com"
        self.user = CustomUser.objects.create_user(username=username, password=password, email=email)

        # Create category and product
        category = Category.objects.create(name='Electronics')
        self.product = Product.objects.create(
            name='Product 1',
            description='Description',
            price=10000,
            stock_quantity=100,
            category=category
        )

        # Create shopping cart and add product
        cart = ShoppingCart.objects.create(user=self.user)
        self.cart = cart

        self.data = {
            'username': username,
            'password': password
        }
    
    def test_create_order(self):
        client = APIClient()
        token = client.post('/api/auth/token/', self.data)
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token.data['access'])

        CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)
        
        response = client.post('/api/orders/', {})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'order is created successfully')
    
    def test_create_order_empty_cart(self):
        client = APIClient()
        token = client.post('/api/auth/token/', self.data)
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token.data['access'])

        response = client.post('/api/orders/', {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Error', response.data)

