from django.urls import path

from .views import CreditDetailView, CreditIndexView, InstitutionDetailView, InstitutionIndexView, InstructorDetailView, \
    InstructorIndexView

app_name = 'Education'
urlpatterns = [
    path('class/<int:pk>/', CreditDetailView.as_view(), name='credit-detail'),
    path('school/<int:pk>/', InstitutionDetailView.as_view(), name='institution-detail'),
    path('teacher/<int:pk>/', InstructorDetailView.as_view(), name='teacher-detail'),
    path('classes', CreditIndexView.as_view(), name='classes'),
    path('teachers', InstructorIndexView.as_view(), name='instructors'),
    path('schools', InstitutionIndexView.as_view(), name='schools'),
]
