from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DetailView, ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView

from .forms import PersonForm
from .models import Institution, Credit


class AddressView(FormView):
    template_name = 'Education/address.html'
    form_class = PersonForm
    success_url = '/thanks/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super().form_valid(form)


class CreditCreate(CreateView):
    model = Credit


class CreditDelete(DeleteView):
    model = Credit
    success_url = reverse_lazy('credit-detail')


class CreditDetailView(DetailView):
    model = Credit
    template_name = 'Education/credit_detail.html'


class CreditIndexView(ListView):
    model = Credit

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class CreditUpdate(UpdateView):
    model = Credit
    template_name_suffix = '_update_form'


class IndexView(TemplateView):
    template_name = 'base.html'


class InstitutionCreate(CreateView):
    model = Institution


class InstitutionDelete(DeleteView):
    model = Institution
    success_url = reverse_lazy('institution-detail')


class InstitutionDetailView(DetailView):
    model = Institution
    template_name = 'Education/institution_detail.html'


class InstitutionIndexView(ListView):
    model = Institution

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    def net_cost(self):
        net_tuition = self.next_year_full_tuition - Institution.financial_aid_awarded
        return net_tuition


class InstitutionUpdate(UpdateView):
    model = Institution
    template_name_suffix = '_update_form'
