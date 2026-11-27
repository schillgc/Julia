"""Read the company name from a Mailchimp account using local environment credentials."""

import os

from mailchimp3 import MailChimp


def main():
    api_key = os.environ.get("JOB_SEARCH_MAILCHIMP_API_KEY", "").strip()
    username = os.environ.get("JOB_SEARCH_MAILCHIMP_USERNAME", "").strip()
    if not api_key or not username:
        raise SystemExit(
            "Set JOB_SEARCH_MAILCHIMP_API_KEY and JOB_SEARCH_MAILCHIMP_USERNAME "
            "before running this utility."
        )

    try:
        client = MailChimp(mc_api=api_key, mc_user=username)
        company = client.lists.all(get_all=True, fields="lists.contact.company")
    except Exception:
        raise SystemExit(
            "Mailchimp API request failed. Check network connectivity and local credentials."
        ) from None

    print(company)


if __name__ == "__main__":
    main()
