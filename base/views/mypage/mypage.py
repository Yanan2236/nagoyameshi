from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from base.models import Favorite, Review, Reservation

class MyPageView(LoginRequiredMixin, TemplateView):
    template_name = "base/mypage/index.html"
    login_url = "account_login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context["my_reservations"] = (
            Reservation.objects
            .filter(user=self.request.user)
            .select_related("restaurant")
            .order_by("reserved_datetime")
        )
        
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