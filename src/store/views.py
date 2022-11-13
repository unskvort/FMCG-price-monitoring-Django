from collections import Counter
from typing import Any, Type

from django.db.models import Model
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from store.models import Category, Product


class Home(ListView):
    model: Type[Model] = Product
    template_name: str = "index.html"
    paginate_by: int = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Список товаров"
        return context

    def get_queryset(self):
        queryset = Product.objects.all().select_related("category").order_by("id")
        return queryset


class WithinCategory(ListView):
    model: Type[Model] = Product
    template_name: str = "category.html"
    context_object_name: str = "products"
    paginate_by: int = 5

    def get_queryset(self):
        queryset = (
            Product.objects.filter(category_id=self.kwargs["category_id"]).select_related("category").order_by("id")
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cur_category"] = get_object_or_404(Category, pk=self.kwargs["category_id"])
        return context


class ViewProduct(DetailView):
    model: Type[Model] = Product
    template_name: str = "product.html"
    context_object_name: str = "product_item"

    def _prepare_chart(self, prices: QuerySet) -> tuple[tuple[Any | int], tuple[Any | int]]:
        data: Counter = Counter()
        for row in prices:
            yymm = row.updated_at.strftime("%d/%m/%Y")
            price = row.price
            data[yymm] = price

        labels, values = zip(*data.items())
        return labels, values

    def get_object(self):
        object = get_object_or_404(Product.objects.select_related(), pk=self.kwargs["product_id"])
        return object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        prices = Product.objects.get(pk=self.kwargs["product_id"]).price_records.all()  # type: ignore
        labels, values = self._prepare_chart(prices)
        context["prices"] = prices
        context["labels"] = labels
        context["values"] = values
        return context
