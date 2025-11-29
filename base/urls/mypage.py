from django.urls import path
from base.views.mypage.mypage import MyPageView
from base.views.mypage.user_name import UserNameUpdateView


urlpatterns = [
    path("", MyPageView.as_view(), name="mypage"),
    path("username/edit/", UserNameUpdateView.as_view(), name="username_update"),
]