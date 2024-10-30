from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DetailView, ListView, CreateView, DeleteView, UpdateView

from .forms import PersonForm, CreditForm
from .models import Credit, School, Instructor

import math


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


class AddressView(CreateView):
    """ Description: This view handles the form for entering a person's address. """
    template_name = 'education/address.html'
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
    template_name = 'education/credit_form.html'
    form_class = CreditForm
    success_url = reverse_lazy('education:credit-detail', kwargs={'slug': Credit.slug})


class CreditDeleteView(DeleteView):
    """ Description: Handles the deletion of a "Credit" instance. """
    model = Credit
    success_url = reverse_lazy('education:credit-detail')


class CreditDetailView(DetailView):
    """ Description: Displays the details of a specific "Credit" instance. """
    model = Credit
    template_name = 'education/credit_detail.html'


class CreditIndexView(ListView):
    """ Description: Displays a list of all "Credit" instances. """
    model = Credit
    template_name = 'education/credit_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    def truncate(number, digits) -> float:
        # Improve accuracy with floating point operations, to avoid truncate(16.4, 2) = 16.39 or truncate(-1.13, 2) = -1.12
        nbDecimals = len(str(number).split('.')[1])
        if nbDecimals <= digits:
            return number
        stepper = 10.0 ** digits
        return math.trunc(stepper * number) / stepper


class CreditUpdateView(UpdateView):
    """ Description: Handles the update of a specific "Credit" instance. """
    model = Credit
    template_name_suffix = '_update_form'


class IndexView(ListView):
    """ Description: The main entry point of the web application. """
    template_name = 'base.html'
    context_object_name = 'credit_list'
    paginate_by = 10  # Adjust as needed, or set to None for no pagination

    def get_queryset(self):
        return Credit.objects.all().order_by()  # Adjust the ordering as needed

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any additional context data if needed
        return context


class InstitutionCreateView(CreateView):
    """ Description: Handles the creation of a new "Institution" instance. """
    model = School
    template_name = 'education/institution_form.html'


class InstitutionDeleteView(DeleteView):
    """ Description: Handles the deletion of an "Institution" instance. """
    model = School
    success_url = reverse_lazy('institution-detail')


class InstitutionDetailView(DetailView):
    """ Description: Displays the details of a specific "Institution" instance. """
    model = School
    # template_name = 'Education/institution_detail.html'


class InstitutionIndexView(ListView):
    """ Description: Displays a list of all "Institution" instances. """
    model = School
    template_name = 'Education/institution_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    @staticmethod
    def net_cost():
        net_tuition = School.next_year_full_tuition - School.financial_aid_awarded
        return net_tuition


class InstitutionUpdateView(UpdateView):
    """ Description: Handles the update of a specific "Institution" instance. """
    model = School
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
