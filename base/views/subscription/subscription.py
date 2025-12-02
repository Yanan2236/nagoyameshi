from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.generic import View, TemplateView
from datetime import timedelta
import stripe

from base.models import Subscription
from base.mixins import SubscriptionRequiredMixin


stripe.api_key = settings.STRIPE_SECRET_KEY


class SubscriptionCreateView(LoginRequiredMixin, View):
    login_url = "account_login"

    def get(self, request, *args, **kwargs):
        return render(request, "base/subscription/subscription_create.html")

    def post(self, request, *args, **kwargs):
        user = request.user

        success_url = request.build_absolute_uri(
            reverse("subscription_success")
        ) + "?session_id={CHECKOUT_SESSION_ID}"
        cancel_url = request.build_absolute_uri(
            reverse("subscription_cancel")
        )

        billing = getattr(user, "billing", None)
        customer_id = billing.stripe_customer_id if billing and billing.stripe_customer_id else None

        session_params = dict(
            mode="payment",
            line_items=[
                {
                    "price": settings.STRIPE_SUBSCRIPTION_PRICE_ID,
                    "quantity": 1,
                }
            ],
            success_url=success_url,
            cancel_url=cancel_url,
        )

        if customer_id:
            session_params["customer"] = customer_id
        else:
            session_params["customer_email"] = user.email

        session = stripe.checkout.Session.create(**session_params)

        return redirect(session.url, permanent=False)


def subscription_success(request):
    session_id = request.GET.get("session_id")
    if not session_id:
        return redirect("mypage")

    checkout_session = stripe.checkout.Session.retrieve(session_id)

    if checkout_session.payment_status == "paid":
        user = request.user
        started = timezone.now()
        ended = started + timedelta(days=30)

        sub, created = Subscription.objects.get_or_create(
            user=user,
            defaults={"started_at": started, "ended_at": ended},
        )
        if not created:
            sub.started_at = started
            sub.ended_at = ended
            sub.save()

    return render(request, "base/subscription/subscription_success.html")


class SubscriptionCancelView(SubscriptionRequiredMixin, TemplateView):
    login_url = "account_login"
    template_name = "base/subscription/subscription_cancel.html"

    def post(self, request, *args, **kwargs):
        sub = request.user.subscription
        sub.ended_at = timezone.now()
        sub.save()
        return redirect("mypage")
