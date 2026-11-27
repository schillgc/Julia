from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

from .forms import CompanyForm, ContactForm
from .models import Company, Position


@method_decorator(staff_member_required(login_url="/admin/login/"), name="dispatch")
class CompanyIndexView(ListView):
    model = Company
    paginate_by = 100


@method_decorator(staff_member_required(login_url="/admin/login/"), name="dispatch")
class CompanyDetailView(DetailView):
    model = Company
    template_name = "theanalyzer/company_detail.html"
    slug_url_kwarg = 'the_slug'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    def list(request):
        company_list = Company.objects.all()
        return render(request, 'company_list.html', {'company_list': company_list})


class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = '/thanks/'

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)


@method_decorator(staff_member_required(login_url="/admin/login/"), name="dispatch")
class LogoImage(TemplateView):
    form = CompanyForm
    template_name = 'company_logo.html'

    def post(self, request, *args, **kwargs):
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('home', kwargs={'pk': pk}))
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


@method_decorator(staff_member_required(login_url="/admin/login/"), name="dispatch")
class PositionDetailView(DetailView):
    model = Position
    template_name = "theanalyzer/position_detail.html"
    slug_url_kwarg = 'the_slug'
    slug_field = 'slug'

    def list(request):
        position_list = Position.objects.all()
        return render(request, 'position_list.html', {'position_list': position_list})


@method_decorator(staff_member_required(login_url="/admin/login/"), name="dispatch")
class PositionIndexView(ListView):
    model = Position
    paginate_by = 100


position_detail_view = PositionDetailView.as_view()
