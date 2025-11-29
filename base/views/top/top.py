from django.views.generic import TemplateView
from base.forms import SearchForm
from base.models import Restaurant

class TopView(TemplateView):
    template_name = "base/top/top.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = SearchForm()

        # --- テスト用：全レストランをトップに表示するためのデータ ---
        context["restaurants"] = Restaurant.objects.all()

        return context
