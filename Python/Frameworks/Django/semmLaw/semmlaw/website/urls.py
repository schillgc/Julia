from django.urls import path

from .views import index, Bio, news

urlpatterns = [
    path('', index, name='index'),
    path('firm/<slug:slug>/', Bio.as_view(), name='attorney_bio'),
    path('firm/<slug:slug>/news', news, name='news'),
]
