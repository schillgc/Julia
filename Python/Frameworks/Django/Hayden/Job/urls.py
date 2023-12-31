from django.urls import path

from .views import CareerDetailView, CareerIndexView

app_name = 'Job'
urlpatterns = [
    path('job/<slug>/', CareerDetailView.as_view(), name='career-detail'),
    path('', CareerIndexView.as_view()),
]
