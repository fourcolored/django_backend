from django.db import models
from .order import Order
from django.conf import settings

class Payment(models.Model):
    PAYMENT_METHODS = [
        ('paypal', 'Paypal'), 
        ('credit_card', 'Credit card'), 
        ('bank_transfer', 'Bank transfer'),
    ]
    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
    ]
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS)
    amount = models.IntegerField()
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['order'])
        ]
    
