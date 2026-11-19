"""Mailchimp Transactional API connectivity check.

Set MAILCHIMP_TRANSACTIONAL_API_KEY in the local environment. Never commit
real API credentials or a local .env file.
"""

import os

import mailchimp_transactional as MailchimpTransactional
from mailchimp_transactional.api_client import ApiClientError

api_key = os.environ.get("MAILCHIMP_TRANSACTIONAL_API_KEY", "")
if not api_key.strip():
    raise SystemExit("Set MAILCHIMP_TRANSACTIONAL_API_KEY before running this example.")

try:
    mailchimp = MailchimpTransactional.Client(api_key)
    response = mailchimp.users.ping()
    print("Mailchimp Transactional API connection succeeded.")
except ApiClientError as error:
    print("Mailchimp Transactional API request failed: {}".format(error.text))
    raise SystemExit(1) from error
