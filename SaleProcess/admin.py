from django.contrib import admin
from .models import Cart

class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_name', 'user',)
    list_filter = ('user',)

admin.site.register(Cart, CartAdmin)

