from django.views import generic

from .models import Phone
class PhoneDetailView(generic.DetailView):
    model = Phone
    template_name = 'biller/detail.html'

class PhoneListView(generic.ListView):
    model = Phone
    template_name = 'biller/account.html'
