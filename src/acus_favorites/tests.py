import tempfile

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from acus_favorites.models import Favorite
from acus_store.models import Category, PriceRecord, Product


class FavoriteTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="test", password="test", email="test@mail.com")
        user.save()
        image = tempfile.NamedTemporaryFile(suffix=".jpg").name
        category = Category.objects.create(name="test")
        product = Product.objects.create(
            article=12,
            name="test",
            category=category,
            image=image,
            price=123,
        )
        PriceRecord.objects.create(product=product, price=123)
        Favorite.objects.create(user=user, product=product)

    def test_favorite_anonym(self):
        response = self.client.get(reverse("favorites"))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_favorite_user(self):
        login = self.client.login(username="test", password="test")
        response = self.client.get(reverse("favorites"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
