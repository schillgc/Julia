from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .models import Company, Position
from .views import CompanyIndexView, CompanyDetailView, PositionIndexView, PositionDetailView

app_name = 'theanalyzer'
urlpatterns = [
    path('positions/', PositionIndexView.as_view(model=Position), name='position_list'),
    path('position/<slug:the_slug>/', PositionDetailView.as_view(), name='position_detail'),
    path('companies/', CompanyIndexView.as_view(model=Company), name='company_list'),
    path('company/<int:pk>/', CompanyDetailView.as_view(), name='company_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
