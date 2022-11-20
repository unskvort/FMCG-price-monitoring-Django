from typing import Any
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView

from acus_auth.forms import RegisterUser
from acus_auth.utils import anonymous_required


class Logout(LogoutView):
    def get_default_redirect_url(self) -> str:
        return "/"


class Login(LoginView):
    template_name: str = "authentication/login.html"
    redirect_authenticated_user = True
    extra_context = {"title": "Авторизация"}

    def get_default_redirect_url(self) -> str:
        return "/"


@method_decorator(anonymous_required, name="dispatch")
class Register(CreateView):
    form_class = RegisterUser
    success_url = reverse_lazy("login")
    template_name: str = "authentication/register.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Регистрация"
        return context
