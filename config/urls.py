from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("base.urls.top")),
    path("restaurants/", include("base.urls.restaurants")),
    path("api/", include("base.urls.api")),
    path("accounts/", include("allauth.urls")),
    path("mypage/", include("base.urls.mypage")),
    path("reviews/", include("base.urls.review")),
]
