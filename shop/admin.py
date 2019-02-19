from django.contrib import admin
from .models import Shop, Item


@admin.register(Shop)  # 장식자 (Decorators)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'created_at']


@admin.register(Item)  # 장식자 (Decorators)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'is_public', 'created_at']
