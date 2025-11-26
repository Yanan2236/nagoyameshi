from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import View, TemplateView
from django.utils import timezone
from datetime import timedelta
import stripe

from base.models import Subscription
from base.mixins import CardRequiredMixin, SubscriptionRequiredMixin
from base.services.stripe import charge_subscription
    

class SubscriptionCreateView(CardRequiredMixin, View):
    login_url = "account_login" # AllauthのログインURLを指定
    
    def get(self, request, *args, **kwargs):
        return render(request, "base/subscription/subscription_create.html")
    
    def post(self, request, *args, **kwargs):
        user = request.user        
        charge_subscription(user, amount_jpy=300)
        
        sub = getattr(user, 'subscription', None)
        
        started = timezone.now()
        ended = started + timedelta(days=30)  # 30日間のサブスクリプション
        
        if sub:
            sub.started_at = started
            sub.ended_at = ended
            sub.save()
        else:
            Subscription.objects.create(
                user=user,
                started_at=started,
                ended_at=ended
            )
            
        return redirect("subscription_success")


def subscription_success(request):
    return render(request, "base/subscription/subscription_success.html")

class SubscriptionCancelView(SubscriptionRequiredMixin, TemplateView):
    login_url = "account_login" # AllauthのログインURLを指定
    template_name = "base/subscription/subscription_cancel.html"
    
    def post(self, request, *args, **kwargs):
        sub = request.user.subscription
        sub.ended_at = timezone.now()
        sub.save()
        return redirect("mypage")
    
    

        
            