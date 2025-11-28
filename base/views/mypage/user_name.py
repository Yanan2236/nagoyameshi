from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

class UserNameUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    fields = ['username']
    template_name = "base/mypage/user_name.html"
    success_url = reverse_lazy("mypage")
    login_url = "account_login"
    
    def get_object(self):
        return self.request.user