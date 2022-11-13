import tempfile

from django.contrib.auth.models import User
from django.core.files.images import ImageFile
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from parse.download import Downloader
from store.models import Category, PriceRecord, Product


class DjangoViews(TestCase):
    @classmethod
    def setUpTestData(cls):
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

    def test_homapage(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_category(self):
        response = self.client.get("/category/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product(self):
        response = self.client.get("/product/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_swagger(self):
        response = self.client.get("/swagger/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class APIViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", email="test@mail.com", password="test")
        self.with_auth = APIClient()
        refresh = RefreshToken.for_user(self.user)
        self.with_auth.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    def test_current_user(self):
        self.assertEqual(self.user.is_active, 1, "Active User")

    def test_authentication(self):
        response = self.client.get("/api/v1/prices/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_prices(self):
        response = self.with_auth.get("/api/v1/prices/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # type: ignore

    def test_categories(self):
        response = self.with_auth.get("/api/v1/categories/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # type: ignore

    def test_products(self):
        response = self.with_auth.get("/api/v1/products/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # type: ignore


class Parser(TestCase):
    def setUp(self):
        self.downloader = Downloader()
        self.categories = self.downloader.categories()
        self.products = self.downloader.products(self.categories[0])
        self.image = self.downloader.image(
            url="https://ssl.gstatic.com/ui/v1/icons/mail/rfr/logo_gmail_lockup_dark_1x_r5.png",
            name="test",
        )

    def test_categories(self):
        self.assertIsInstance(self.categories, list)

    def test_products(self):
        self.assertIsInstance(self.products, dict)

    def test_image(self):
        self.assertIsInstance(self.image, ImageFile)
