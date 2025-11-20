from django.urls import path, include

urlpatterns = [
    path("restaurants/", include("base.urls.restaurants")),
    path("users/", include("base.urls.users")),
    path("reservations/", include("base.urls.reservations")),
]