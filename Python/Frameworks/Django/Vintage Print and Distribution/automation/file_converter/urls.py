from django.urls import path

from . import views

urlpatterns = [
    path('<int:question_id>/', views.demographics, name='demographics'),
]
