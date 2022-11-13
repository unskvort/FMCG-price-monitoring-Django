from django.db import models
from django.urls import reverse


class Category(models.Model):
    class Meta:
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=150, db_index=True)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse("category", kwargs={"category_id": self.pk})


class Product(models.Model):

    article = models.IntegerField(unique=True)
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, models.CASCADE, related_name="products")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField()
    price = models.IntegerField()

    def __str__(self):
        return self.name

    def get_absolute_url(self) -> str:
        return reverse("product", kwargs={"product_id": self.pk})


class PriceRecord(models.Model):

    product = models.ForeignKey(Product, models.CASCADE, related_name="price_records")
    price = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.product)
