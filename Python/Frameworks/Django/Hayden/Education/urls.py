from django.urls import path

from .views import (
    AddressView, CreditCreateView, CreditDeleteView, CreditDetailView, CreditIndexView, CreditUpdateView,
    IndexView, InstitutionCreateView, InstitutionDeleteView, InstitutionDetailView, InstitutionIndexView,
    InstitutionUpdateView, InstructorCreateView, InstructorDeleteView, InstructorDetailView, InstructorIndexView,
    InstructorUpdateView
)

app_name = 'Education'
urlpatterns = [
    path('address/', AddressView.as_view(), name='address'),
    path('class/create/', CreditCreateView.as_view(), name='credit-create'),
    path('class/<slug>/delete/', CreditDeleteView.as_view(), name='credit-delete'),
    path('class/<slug>/', CreditDetailView.as_view(), name='credit-detail'),
    path('classes/', CreditIndexView.as_view(), name='classes'),
    path('class/<slug>/update/', CreditUpdateView.as_view(), name='credit-update'),
    path('', IndexView.as_view(), name='index'),
    path('school/create/', InstitutionCreateView.as_view(), name='institution-create'),
    path('school/<slug>/delete/', InstitutionDeleteView.as_view(), name='institution-delete'),
    path('school/<slug>/', InstitutionDetailView.as_view(), name='institution-detail'),
    path('schools/', InstitutionIndexView.as_view(), name='institution-list'),
    path('school/<slug>/update/', InstitutionUpdateView.as_view(), name='institution-update'),
    path('teacher/create/', InstructorCreateView.as_view(), name='instructor-create'),
    path('teacher/<slug>/delete/', InstructorDeleteView.as_view(), name='instructor-delete'),
    path('teacher/<slug>/', InstructorDetailView.as_view(), name='teacher-detail'),
    path('teachers/', InstructorIndexView.as_view(), name='instructor-list'),
    path('teacher/<slug>/update/', InstructorUpdateView.as_view(), name='instructor-update'),
]
