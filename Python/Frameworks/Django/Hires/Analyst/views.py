from django.views.generic import DetailView, ListView

from .models import Job


class IndexView(ListView):
    template_name = 'Analyst/index.html'
    context_object_name = 'job_list'

    def get_queryset(self):
        return Job.objects.order_by('title')


class DetailView(DetailView):
    model = Job
    template_name = 'Analyst/detail.html'
