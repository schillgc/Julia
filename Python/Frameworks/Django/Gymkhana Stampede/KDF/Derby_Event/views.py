from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, "index.html")


def landing_page(request):
    return render(request, "landing_page.html")


def login(request):
    return render(request, "login.html")


def louisville_concierge(request):
    return render(request, "louisville_concierge.html")


def register(request):
    return render(request, "register.html")


def rules(request):
    return render(request, "rules.html")
