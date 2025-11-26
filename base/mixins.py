from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin


class SubscriptionRequiredMixin(LoginRequiredMixin):
    login_url = "account_login"  # AllauthのログインURLを指定

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return self.handle_no_permission() # LoginRequiredMixinの処理を利用
        
        subscription = getattr(user, 'subscription', None)
        if not (subscription and subscription.is_active):
            return redirect("subscription_create")
        
        return super().dispatch(request, *args, **kwargs) # 次のdispatchへ
    
    
class CardRequiredMixin(LoginRequiredMixin):
    login_url = "account_login"  # AllauthのログインURLを指定

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        billing = getattr(user, 'billing', None)
        if not (billing and billing.default_payment_method_id):
            return redirect("card_update")
        
        return super().dispatch(request, *args, **kwargs)
