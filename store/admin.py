from django.contrib import admin
from .models import Product


class ProductAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,      {'fields': ['in_stock']}),
        ('Описание',{'fields': ['name', 'price', 'description']}),
        ('Фото',   {'fields': ['image1', 'image2', 'image3']}),
        ('Видео',   {'fields': ['video']}),
    ]
    list_display = ('name', 'price', 'in_stock')
admin.site.register(Product, ProductAdmin)