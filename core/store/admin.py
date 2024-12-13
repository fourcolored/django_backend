from django.contrib import admin
from .models import *

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Payment)
admin.site.register(Order)
admin.site.register(WishList)
admin.site.register(WishListItem)
