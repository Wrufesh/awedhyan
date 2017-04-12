from braces.views import LoginRequiredMixin
from django.views.generic import TemplateView


class HomeView(TemplateView, LoginRequiredMixin):
    template_name = 'home.html'

    # def get_context_data(self, **kwargs):
    #     context = super(HomeView, self).get_context_data(**kwargs)
    #     context = RequestContext(self.request)
    #     return context
