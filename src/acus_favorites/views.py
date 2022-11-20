from typing import Any, Type

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Model
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import ListView

from acus_favorites.models import Favorite
from acus_store.models import Product


class ManagerFavorites(View):
    def post(self, request) -> HttpResponseRedirect:
        product = get_object_or_404(Product, id=request.POST.get("id"))
        favorite, create_flag = Favorite.objects.get_or_create(user=request.user, product=product)
        if not create_flag:
            favorite.delete()
        return HttpResponseRedirect(request.META["HTTP_REFERER"])


class ShowFavorites(LoginRequiredMixin, ListView):
    model: Type[Model] = Favorite
    template_name: str = "favorites/dashboard.html"

    def get_queryset(self) -> QuerySet[Favorite]:
        queryset = Favorite.objects.filter(user=self.request.user).select_related("product__category")
        return queryset

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Избранное"
        return context
