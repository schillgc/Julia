from django.urls import path

from . import views


app_name = 'Analyst'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('job/<slug:slug>/', views.DetailView.as_view(), name='detail'),
]
