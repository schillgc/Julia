from mailchimp3 import MailChimp


client = MailChimp('YOUR_USERNAME', 'YOUR_SECRET_KEY')


title = input("Position Title ")
institution_name = input("Institution ")
contact_name = input("Contact's Name ")
contact_phone = input("Phone Number ")
contact_email = input("Email Address ")
landing_status = input("Status ")
prospects = (
                title,
                institution_name,
                contact_name,
                contact_phone,
                contact_email,
                landing_status
)
