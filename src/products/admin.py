from django.contrib import admin

from base.admin import BaseModelAdmin

from .models import Category, Product


class ProductInLine(admin.TabularInline):
    model = Product
    extra = 0


@admin.register(Category)
class CategoryAdmin(BaseModelAdmin):
    list_display = ['title', 'owner', 'created_at']

    inlines = [
        ProductInLine,
    ]


@admin.register(Product)
class ProductAdmin(BaseModelAdmin):
    list_display = ['name', 'category', 'unit_price', 'created_at']

