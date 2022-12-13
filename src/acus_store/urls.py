from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from acus_store import api, views

router = routers.SimpleRouter()
router.register(r"categories", api.CategoryViewSet)
router.register(r"products", api.ProductViewSet)
router.register(r"prices", api.PriceViewSet)

urlpatterns = [
    path("ping/", views.ping, name="ping"),
    path("", views.Home.as_view(), name="homepage"),
    path("search/", views.Searching.as_view(), name="searching"),
    path("category/<int:category_id>/", views.CategoryWithin.as_view(), name="category"),
    path("product/<int:product_id>/", views.ViewProduct.as_view(), name="product"),
    path("api/v1/", include(router.urls)),
    path("api/v1/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/v1/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/v1/token/verify/", TokenVerifyView.as_view(), name="token_refresh"),
]
