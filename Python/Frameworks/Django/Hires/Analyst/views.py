from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView

from .models import Job


@method_decorator(staff_member_required(login_url="/admin/login/"), name="dispatch")
class IndexView(ListView):
    template_name = 'Analyst/index.html'
    context_object_name = 'job_list'

    def get_queryset(self):
        return Job.objects.order_by('title')


@method_decorator(staff_member_required(login_url="/admin/login/"), name="dispatch")
class DetailView(DetailView):
    model = Job
    template_name = 'Analyst/detail.html'
