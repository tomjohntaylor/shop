from django.contrib import admin
from .models import Product, ProductCategory

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'product_category',)
    list_filter = ('product_category',)

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCategory)

