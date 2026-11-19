from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import render
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError

# Mailchimp configuration is supplied through the process environment.
api_key = settings.MAILCHIMP_API_KEY
server = settings.MAILCHIMP_DATA_CENTER
list_id = settings.MAILCHIMP_EMAIL_LIST_ID


def subscribe(email):
    """Create a pending subscription; the recipient must confirm by email."""
    if not all(value and str(value).strip() for value in (api_key, server, list_id)):
        return None

    mailchimp = Client()
    mailchimp.set_config({"api_key": api_key, "server": server})
    member_info = {"email_address": email, "status": "pending"}

    try:
        return mailchimp.lists.add_list_member(list_id, member_info)
    except ApiClientError:
        # Do not write addresses or provider payloads into application logs.
        return None


def subscription(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Enter a valid email address.")
        else:
            response = subscribe(email)
            if response is None:
                messages.error(
                    request,
                    "The subscription could not be submitted. Please try again later.",
                )
            else:
                messages.success(
                    request,
                    "Please check your inbox to confirm your subscription.",
                )

    return render(request, "marketing/index.html")
