from django.urls import path
from base.views.mypage.mypage import MyPageView


urlpatterns = [
    path("", MyPageView.as_view(), name="mypage"),
]