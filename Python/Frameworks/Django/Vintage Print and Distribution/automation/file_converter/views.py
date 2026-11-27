from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, render

from .models import Demographics


@staff_member_required(login_url="/admin/login/")
def demographics(request, address_id):
    address = get_object_or_404(Demographics, pk=address_id)
    return render(
        request,
        "file_converter/address.html",
        {"address": address},
    )
