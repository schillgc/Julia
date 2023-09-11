from django.urls import path

from .views import CreditDetailView, CreditIndexView, InstitutionDetailView, InstitutionIndexView, InstructorDetailView, \
    InstructorIndexView

app_name = 'Education'
urlpatterns = [
    path('class/<slug>/', CreditDetailView.as_view(), name='credit-detail'),
    path('school/<slug>/', InstitutionDetailView.as_view(), name='institution-detail'),
    path('teacher/<slug>/', InstructorDetailView.as_view(), name='teacher-detail'),
    path('classes', CreditIndexView.as_view(), name='classes'),
    path('teachers', InstructorIndexView.as_view(), name='instructors'),
    path('schools', InstitutionIndexView.as_view(), name='schools'),
]
