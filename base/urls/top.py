from django.urls import path
from base.views.top.top import TopView

urlpatterns = [
    path("", TopView.as_view(), name="top"),
]