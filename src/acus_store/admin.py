from django.contrib import admin

from acus_store.models import Category, PriceRecord, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "created_at", "updated_at", "price")
    list_filter = ("category", "updated_at")


@admin.register(PriceRecord)
class PriceAdmin(admin.ModelAdmin):
    list_display = ("product", "updated_at", "price")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
