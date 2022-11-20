from rest_framework import serializers

from acus_store.models import Product, Category, PriceRecord


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "name", "price", "category_id", "created_at", "updated_at")


class PricesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceRecord
        fields = ("product", "price", "updated_at")
