from django.contrib.auth.models import User
from django.db import models

from acus_store.models import Product


class Favorite(models.Model):

    user = models.ForeignKey(User, models.CASCADE, related_name="favorites")
    product = models.ForeignKey(Product, models.CASCADE, related_name="favorites")

    def __str__(self) -> str:
        return str(self.user)
