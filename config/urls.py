from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("base.urls.top")),
    path("restaurants/", include("base.urls.restaurants")),
    path("api/", include("base.urls.api")),
    path("accounts/", include("allauth.urls")),
    path("mypage/", include("base.urls.mypage")),
    path("reviews/", include("base.urls.review")),
    path("billing/", include("base.urls.billing")),
    path("subscription/", include("base.urls.subscription")),
    path("reservations/", include ("base.urls.reservations")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
