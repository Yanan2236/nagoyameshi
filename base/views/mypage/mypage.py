from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from base.models import Favorite, Review

class MyPageView(LoginRequiredMixin, TemplateView):
    template_name = "base/mypage/index.html"
    login_url = "account_login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # favorite
        context["favorite_restaurants"] = (
            Favorite.objects
            .filter(user=self.request.user)
            .select_related("restaurant")
            .order_by("-created_at")
        )
        # review
        context["my_reviews"] = (
            Review.objects
            .filter(user=self.request.user)
            .select_related("restaurant")
            .order_by("-created_at")
        )
        
        return context