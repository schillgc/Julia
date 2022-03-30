from django.shortcuts import render


def index(request):
    return render(request, 'monthly_calendar/calendar.html')
