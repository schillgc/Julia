from django.urls import path

from .views import CreditDetailView, CreditIndexView, InstitutionDetailView, InstitutionIndexView

app_name = 'Education'
urlpatterns = [
    path('class/<int:pk>/', CreditDetailView.as_view(), name='credit-detail'),
    path('school/<int:pk>/', InstitutionDetailView.as_view(), name='institution-detail'),
    path('classes', CreditIndexView.as_view(), name='classes'),
    path('schools', InstitutionIndexView.as_view(), name='schools'),
]
