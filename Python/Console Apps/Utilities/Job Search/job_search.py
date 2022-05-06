from credentials import mc_api, mc_user
from mailchimp3 import MailChimp


client = MailChimp(mc_api, mc_user)
company = client.lists.all(get_all=True, fields="lists.contact.company")
print(company)
