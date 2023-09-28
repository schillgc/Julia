import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
import mailchimp_transactional as MailchimpTransactional
from mailchimp_transactional.api_client import ApiClientError


# try:
#   client = MailchimpMarketing.Client()
#   client.set_config({
#     "api_key": "9d006200f84026629fffec6e0eaa5099",
#     "server": "us14"
#   })
#   response = client.ping.get()
#   print(response)
# except ApiClientError as error:
#   print(error)

try:
  mailchimp = MailchimpTransactional.Client('9d006200f84026629fffec6e0eaa5099-us14')
  response = mailchimp.users.ping()
  print('API called successfully: {}'.format(response))
except ApiClientError as error:
  print('An exception occurred: {}'.format(error.text))
