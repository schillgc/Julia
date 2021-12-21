from django.shortcuts import get_object_or_404, render

from .models import Demographics


def demographics(request, address_id):
    address = get_object_or_404(Demographics, pk=address_id)
    return render(request, 'address.html')
