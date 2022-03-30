import phonenumbers, pytz
from phonenumbers import carrier, geocoder, timezone
from dateutil.tz import gettz
from datetime import datetime

phone_number = "+" + input("What is the phone number including country code? ")

parsed_number = phonenumbers.parse(phone_number, "CH")

Region = geocoder.description_for_number(parsed_number, "en")
Carrier = carrier.name_for_number(parsed_number, "RO", "en")
Timezone = gettz(timezone.time_zones_for_number(parsed_number)[0])

if phone_number == phonenumbers.is_possible_number(parsed_number) or phonenumbers.is_valid_number(parsed_number):
    print(parsed_number)
    if Region:
        print(Region)
    if Carrier:
        print(Carrier)
    print(datetime.now().astimezone(Timezone).strftime("%B %d, %Y  %I:%M %p"))
