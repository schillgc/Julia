from django.urls import path
from . import views

app_name = 'Job'
urlpatterns = [
    # The root of the 'career/' path will show the list of careers.
    path('', views.CareerListView.as_view(), name='career-list'),
    # A path with an integer (the primary key) will show that career's detail page.
    path('<int:pk>/', views.CareerDetailView.as_view(), name='career-detail'),
]
