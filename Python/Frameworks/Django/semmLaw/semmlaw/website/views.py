from django.shortcuts import render
from django.template.response import TemplateResponse
from django.views.generic import DetailView, TemplateView

from . import services
from .models import Attorney, Newsfeed
from .utils.news import query


class Bio(DetailView):
    model = Attorney

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class News(TemplateView):
    def get(self, request=(Attorney.first_name, Attorney.last_name), **kwargs):
        Newsfeed.news = services.get_news(query)
        template_name = "website/index.html"
        return render(request, template_name)


def index(request, template_name="website/index.html"):
    return TemplateResponse(request, template_name)
