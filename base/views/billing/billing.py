from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
import stripe
from django.conf import settings

from base.models import UserBilling
from base.services.stripe import get_or_create_billing, get_or_create_stripe_customer
from base.mixins import CardRequiredMixin

stripe.api_key = settings.STRIPE_SECRET_KEY


class CardUpdateView(LoginRequiredMixin, TemplateView):
    template_name = "base/billing/card_update.html"

    def get(self, request, *args, **kwargs):
        user = request.user

        customer_id = get_or_create_stripe_customer(user)

        intent = stripe.SetupIntent.create(
            customer=customer_id,
        )

        context = {
            "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
            "client_secret": intent.client_secret,
        }
        return render(request, self.template_name, context)


def card_update_complete(request):
    if request.method != "POST" or not request.user.is_authenticated:
        return redirect("card_update")

    pm_id = request.POST.get("payment_method_id")
    if not pm_id:
        return redirect("card_update")

    billing = get_or_create_billing(request.user)

    stripe.Customer.modify(
        billing.stripe_customer_id,
        invoice_settings={"default_payment_method": pm_id},
    )

    pm = stripe.PaymentMethod.retrieve(pm_id)
    card = pm.get("card", {})

    billing.default_payment_method_id = pm_id
    billing.card_brand = card.get("brand")
    billing.card_last4 = card.get("last4")
    billing.save()

    return redirect("card_update_done") 

def card_update_done(request):
    return render(request, "base/billing/card_update_complete.html")


class CardInfoView(CardRequiredMixin, TemplateView):
    login_url = "account_login"  # AllauthのログインURLを指定
    template_name = "base/billing/card_infomation.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["billing"] = getattr(user, 'billing', None)
        return context
    
    
class CardDeleteView(CardRequiredMixin, TemplateView):
    login_url = "account_login"  # AllauthのログインURLを指定
    template_name = "base/billing/card_delete_confirm.html"
    
    def post(self, request, *args, **kwargs):
        user = request.user
        billing = user.billing
        pm_id = billing.default_payment_method_id
        
        stripe.PaymentMethod.detach(pm_id)
    
        billing.default_payment_method_id = None
        billing.card_brand = ""
        billing.card_last4 = ""
        billing.save(update_fields=["default_payment_method_id", "card_brand", "card_last4"])
        
        return redirect("mypage")