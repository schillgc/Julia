from django.urls import path

from . import views

urlpatterns = [
    path('<int:address_id>/', views.demographics, name='demographics'),
]
