from django.contrib import admin
from .models import LockMessage, ShippingAddress
# Register your models here.
admin.site.register(LockMessage)
admin.site.register(ShippingAddress)