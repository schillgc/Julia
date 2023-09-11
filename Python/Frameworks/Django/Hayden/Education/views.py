from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DetailView, ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView

from .forms import PersonForm
from .models import Credit, Institution, Instructor


def calculate_course_gpa(Credit, course_gpa=0):
    if Credit.grade_percentage:
        if Credit.grade_percentage >= 90:
            course_gpa = 4.0
            return course_gpa
        elif Credit.grade_percentage == 89:
            course_gpa = 3.9
            return course_gpa
        elif Credit.grade_percentage == 88:
            course_gpa = 3.8
            return course_gpa
        elif Credit.grade_percentage == 87:
            course_gpa = 3.7
            return course_gpa
        elif Credit.grade_percentage == 86:
            course_gpa = 3.5
            return course_gpa
        elif Credit.grade_percentage == 85:
            course_gpa = 3.4
            return course_gpa
        elif Credit.grade_percentage == 84:
            course_gpa = 3.3
            return course_gpa
        elif Credit.grade_percentage == 83:
            course_gpa = 3.0
            return course_gpa
        elif Credit.grade_percentage == 82:
            course_gpa = 2.9
            return course_gpa
        elif Credit.grade_percentage == 81:
            course_gpa = 2.8
            return course_gpa
        elif Credit.grade_percentage == 80:
            course_gpa = 2.7
            return course_gpa
        elif Credit.grade_percentage == 79:
            course_gpa = 2.5
            return course_gpa
        elif Credit.grade_percentage == 78:
            course_gpa = 2.4
            return course_gpa
        elif Credit.grade_percentage == 77:
            course_gpa = 2.3
            return course_gpa
        elif Credit.grade_percentage == 76:
            course_gpa = 2.1
            return course_gpa
        elif Credit.grade_percentage == 75:
            course_gpa = 1.9
            return course_gpa
        elif Credit.grade_percentage == 74:
            course_gpa = 1.8
            return course_gpa
        elif Credit.grade_percentage == 73:
            course_gpa = 1.7
            return course_gpa
        elif Credit.grade_percentage == 72:
            course_gpa = 1.5
            return course_gpa
        elif Credit.grade_percentage == 71:
            course_gpa = 1.4
            return course_gpa
        elif Credit.grade_percentage == 70:
            course_gpa = 1.3
            return course_gpa
        elif Credit.grade_percentage <= 69:
            course_gpa = 0
            return course_gpa

    if Credit.track:
        if Credit.track == "AP":
            course_gpa += 2
        elif Credit.track == "Advanced":
            course_gpa += 1.6
        elif Credit.track == "Honors":
            course_gpa += 1.2
        elif Credit.track == "Academic":
            course_gpa += 0.8
        elif Credit.track == "Traditional":
            course_gpa += 0


def official_grade_level(Credit):
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
    # template_name = 'Education/credit_detail.html'


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

    @staticmethod
    def net_cost():
        net_tuition = Institution.next_year_full_tuition - Institution.financial_aid_awarded
        return net_tuition


class InstitutionUpdate(UpdateView):
    model = Institution
    template_name_suffix = '_update_form'


class InstructorCreate(CreateView):
    model = Instructor


class InstructorDelete(DeleteView):
    model = Instructor
    success_url = reverse_lazy('instructor-detail')


class InstructorDetailView(DetailView):
    model = Instructor
    template_name = 'Education/instructor_detail.html'


class InstructorIndexView(ListView):
    model = Instructor

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class InstructorUpdate(UpdateView):
    model = Instructor
    template_name_suffix = '_update_form'
