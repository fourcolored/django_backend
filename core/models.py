from django.db import models

# Create your models here.
class Store(models.Model):
    key = models.CharField(max_length=50, unique=True)
    value = models.CharField(max_length=200)
