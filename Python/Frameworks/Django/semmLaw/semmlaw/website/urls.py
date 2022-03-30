from django.urls import path

from .views import index, Bio, News


urlpatterns = [
    path('', index, name='index'),
    path('firm/<slug:slug>/', Bio.as_view(), name='attorney_bio'),
    path('news/', News, name='news'),
]
