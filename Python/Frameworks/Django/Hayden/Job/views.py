from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import Career


class CareerCreate(CreateView):
    model = Career


class CareerDelete(DeleteView):
    model = Career
    success_url = reverse_lazy('career-detail')


class CareerDetailView(DetailView):
    model = Career
    template_name = "Job/career_detail.html"


class CareerIndexView(ListView):
    model = Career

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class CareerUpdate(UpdateView):
    model = Career
    template_name_suffix = '_update_form'
