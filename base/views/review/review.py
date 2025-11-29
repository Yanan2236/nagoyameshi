from django.contrib.auth.mixins import LoginRequiredMixin
from base.mixins import SubscriptionRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DeleteView

from base.models import Restaurant, Review


class RestaurantReviewCreateView(SubscriptionRequiredMixin, CreateView):
    model = Review
    fields = ["rating", "comment"]
    template_name = "base/review/review_form.html"
    login_url = "account_login"

    def dispatch(self, request, *args, **kwargs):
        self.restaurant = get_object_or_404(Restaurant, pk=kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.restaurant = self.restaurant
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("restaurant_detail", kwargs={"pk": self.restaurant.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["restaurant"] = self.restaurant
        return context


class RestaurantReviewUpdateView(SubscriptionRequiredMixin, UpdateView):
    model = Review
    pk_url_kwarg = "review_pk"
    fields = ["rating", "comment"]
    template_name = "base/review/review_form.html"
    login_url = "account_login"

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["restaurant"] = self.object.restaurant
        context["user_review"] = self.object
        return context

    def get_success_url(self):
        return reverse("restaurant_detail", kwargs={"pk": self.object.restaurant.pk})
    

class RestaurantReviewDeleteView(SubscriptionRequiredMixin, DeleteView):
    model = Review
    pk_url_kwarg = "review_pk"
    template_name = "base/review/review_delete.html"
    login_url = "account_login"

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse("restaurant_detail", kwargs={"pk": self.object.restaurant.pk})

