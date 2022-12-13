from collections import Counter
from typing import Any, Type

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Model, Q
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from acus_favorites.models import Favorite
from acus_store.models import Category, Product


def ping(request: HttpRequest) -> HttpResponse:
    return HttpResponse("PONG")


class Home(ListView):
    model: Type[Model] = Product
    template_name: str = "store/index.html"
    paginate_by: int = 15

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Список товаров"
        return context

    def get_queryset(self) -> QuerySet[Product]:
        queryset = Product.objects.all().select_related("category").order_by("id")
        return queryset


class CategoryWithin(ListView):
    model: Type[Model] = Product
    template_name: str = "store/category.html"
    context_object_name: str = "products"
    paginate_by: int = 12

    def get_queryset(self) -> QuerySet[Product]:
        queryset = (
            Product.objects.filter(category_id=self.kwargs["category_id"]).select_related("category").order_by("id")
        )
        return queryset

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["cur_category"] = get_object_or_404(Category, pk=self.kwargs["category_id"])
        return context


class ViewProduct(DetailView):
    model: Type[Model] = Product
    template_name: str = "store/product.html"
    context_object_name: str = "product_item"

    def _prepare_chart(self, prices: QuerySet) -> tuple[tuple[Any | int], tuple[Any | int]]:
        data: Counter[Any] = Counter()
        for row in prices:
            yymm = row.updated_at.strftime("%d/%m/%Y")
            price = row.price
            data[yymm] = price

        labels, values = zip(*data.items())
        return labels, values

    def _is_favorite_user(self) -> bool:
        if self.request.user.is_authenticated:
            try:
                Favorite.objects.get(user=self.request.user, product=self.kwargs["product_id"])
                is_favorite = True
            except ObjectDoesNotExist:
                is_favorite = False
            return is_favorite
        else:
            return False

    def get_object(self) -> Product:
        object = get_object_or_404(Product.objects.select_related(), pk=self.kwargs["product_id"])
        return object

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        is_favorite = self._is_favorite_user()
        prices = Product.objects.get(pk=self.kwargs["product_id"]).price_records.all()
        labels, values = self._prepare_chart(prices)
        context["prices"] = prices
        context["is_favorite"] = is_favorite
        context["labels"] = labels
        context["values"] = values
        return context


class Searching(ListView):
    model: Type[Model] = Product
    template_name: str = "store/searching.html"
    context_object_name: str = "searching_list"

    def get_queryset(self) -> QuerySet[Product]:
        query = self.request.GET.get("query")
        queryset = Product.objects.filter(Q(name__icontains=query) | Q(category__name__icontains=query)).select_related(
            "category"
        )
        return queryset

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Поиск"
        return context
