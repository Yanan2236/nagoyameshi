from django.urls import path
from base.views.subscription.subscription import SubscriptionCreateView, subscription_success, SubscriptionCancelView

urlpatterns = [
    path("create/", SubscriptionCreateView.as_view(), name="subscription_create"),
    path("success/", subscription_success, name="subscription_success"),
    path("cancel/", SubscriptionCancelView.as_view(), name="subscription_cancel"),
]