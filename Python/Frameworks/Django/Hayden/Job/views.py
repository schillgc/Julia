from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import Career


@method_decorator(staff_member_required(login_url="/admin/login/"), name="dispatch")
class CareerCreate(CreateView):
    model = Career
    fields = ['profession', 'average_salary', 'required_education']
    success_url = reverse_lazy('Job:career-list')


@method_decorator(staff_member_required(login_url="/admin/login/"), name="dispatch")
class CareerDelete(DeleteView):
    model = Career
    # On success, redirect to the list of careers. The previous URL was incorrect
    # because 'career-detail' requires a primary key (pk).
    success_url = reverse_lazy('Job:career-list')


class CareerListView(ListView):
    model = Career
    # By default, this view uses the template 'Job/career_list.html'
    # and provides the context object 'career_list', which matches the tests.


class CareerDetailView(DetailView):
    model = Career
    # This template name is the default, but explicitly stating it is fine.
    template_name = "Job/career_detail.html"


@method_decorator(staff_member_required(login_url="/admin/login/"), name="dispatch")
class CareerUpdate(UpdateView):
    model = Career
    fields = ['profession', 'average_salary', 'required_education']
    template_name_suffix = '_update_form'

    # It's good practice to define a success_url.
    # Redirecting to the detail view of the updated object is a common pattern.
    def get_success_url(self):
        return reverse_lazy('Job:career-detail', kwargs={'pk': self.object.pk})
