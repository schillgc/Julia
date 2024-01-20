from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DetailView, ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView

from .forms import PersonForm
from .models import Credit, Institution, Instructor


def official_grade_level(Credit):
    """ Description: A standalone function to calculate the grade level based on the total number of classes for a
    "Credit" instance."""
    if Credit.total_classes:
        if Credit.total_classes < 7:
            grade = "Freshman"
        elif Credit.total_classes < 14.5:
            grade = "Sophomore"
        elif Credit.total_classes < 22:
            grade = "Junior"
        elif Credit.total_classes >= 22:
            grade = "Senior"


class AddressView(FormView):
    """ Description: This view handles the form for entering a person's address. """
    template_name = 'Education/address.html'
    form_class = PersonForm
    success_url = '/thanks/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super().form_valid(form)


class CreditCreateView(CreateView):
    """ Description: Handles the creation of a new "Credit" instance. """
    model = Credit
    # template_name = 'Education/credit_form.html'
    # success_url = reverse_lazy('credit-detail/<slug>')


class CreditDeleteView(DeleteView):
    """ Description: Handles the deletion of a "Credit" instance. """
    model = Credit
    success_url = reverse_lazy('credit-detail')


class CreditDetailView(DetailView):
    """ Description: Displays the details of a specific "Credit" instance. """
    model = Credit
    # template_name = 'Education/credit_detail.html'


class CreditIndexView(ListView):
    """ Description: Displays a list of all "Credit" instances. """
    model = Credit
    # template_name = 'Education/credit_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class CreditUpdateView(UpdateView):
    """ Description: Handles the update of a specific "Credit" instance. """
    model = Credit
    template_name_suffix = '_update_form'


class IndexView(TemplateView):
    """ Description: The main entry point of the web application. """
    template_name = 'base.html'


class InstitutionCreateView(CreateView):
    """ Description: Handles the creation of a new "Institution" instance. """
    model = Institution
    # template_name = 'Education/institution_form.html'


class InstitutionDeleteView(DeleteView):
    """ Description: Handles the deletion of an "Institution" instance. """
    model = Institution
    success_url = reverse_lazy('institution-detail')


class InstitutionDetailView(DetailView):
    """ Description: Displays the details of a specific "Institution" instance. """
    model = Institution
    # template_name = 'Education/institution_detail.html'


class InstitutionIndexView(ListView):
    """ Description: Displays a list of all "Institution" instances. """
    model = Institution
    template_name = 'Education/institution_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    @staticmethod
    def net_cost():
        net_tuition = Institution.next_year_full_tuition - Institution.financial_aid_awarded
        return net_tuition


class InstitutionUpdateView(UpdateView):
    """ Description: Handles the update of a specific "Institution" instance. """
    model = Institution
    template_name_suffix = '_update_form'


class InstructorCreateView(CreateView):
    """ Description: Handles the creation of a new "Instructor" instance. """
    model = Instructor
    # template_name = 'Education/instructor_form.html'


class InstructorDeleteView(DeleteView):
    """ Description: Handles the deletion of an "Instructor" instance. """
    model = Instructor
    success_url = reverse_lazy('instructor-detail')


class InstructorDetailView(DetailView):
    """ Description: Displays the details of a specific "Instructor" instance. """
    model = Instructor
    # template_name = 'Education/instructor_detail.html'


class InstructorIndexView(ListView):
    """ Description: Displays a list of all "Instructor" instances. """
    model = Instructor
    # template_name = 'Education/instructor_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class InstructorUpdateView(UpdateView):
    """ Description: Handles the update of a specific "Instructor" instance. """
    model = Instructor
    template_name_suffix = '_update_form'