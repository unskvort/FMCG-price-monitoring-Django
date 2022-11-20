from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status


class AuthTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="test", email="test@mail.com")
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_register_page(self):
        response = self.client.get("/register")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "Регистрация")

    def test_login_page(self):
        response = self.client.get("/login")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "Авторизация")

    def test_logout_page(self):
        response = self.client.get("/logout")
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_register_view_with_login_user(self):
        login = self.client.login(username="test", password="test")
        response = self.client.post(reverse("register"))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_register_view_new_user(self):
        data = {"username": "test1", "password1": "teasda232sdst", "password2": "teasda232sdst"}
        response = self.client.post(reverse("register"), data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
