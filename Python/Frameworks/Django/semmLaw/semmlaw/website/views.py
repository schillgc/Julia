from django.shortcuts import render
from django.template.response import TemplateResponse
from django.views.generic import DetailView
import requests
from .models import Attorney

def news(request):
    url = ('https://newsapi.org/v2/everything?q="{{ Attorney.first_name }} {{ Attorney.last_name }}"'
           'country=us&'
           'apiKey=164788cbd69e4dba8b1f3b57014cd86b')

    attorney_news = requests.get(url).json()

    a = attorney_news['articles']
    desc =[]
    title =[]
    img =[]

    for i in range(len(a)):
        f = a[i]
        title.append(f['title'])
        desc.append(f['description'])
        img.append(f['urlToImage'])
    mylist = zip(title, desc, img)

    context = {'mylist': mylist}

    return render(request, 'news.html', context)


class Bio(DetailView):
    model = Attorney

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context



def index(request, template_name="website/index.html"):
    return TemplateResponse(request, template_name)
