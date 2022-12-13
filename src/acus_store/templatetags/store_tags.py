from django import template
from django.db.models import Count

from acus_store.models import Category

register = template.Library()


@register.inclusion_tag("store/list_categories.html")
def show_categories() -> dict[str, Category]:
    categories = Category.objects.annotate(cnt=Count("products")).filter(cnt__gt=0)
    return {"categories": categories}
