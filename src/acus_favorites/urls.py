from django.urls import path

from acus_favorites import views

urlpatterns = [
    path("manager_favorites/", views.ManagerFavorites.as_view(), name="manager_favorites"),
    path("favorites/", views.ShowFavorites.as_view(), name="favorites"),
]
