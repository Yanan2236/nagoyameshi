from django.views.generic import TemplateView
from base.forms import SearchForm

class TopView(TemplateView):
    template_name = "base/top/top.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = SearchForm()
        return context