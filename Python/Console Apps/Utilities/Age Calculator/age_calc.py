from datetime import date

" Asks user's data "
while True:
    your_name = input("Hello!  What is your name?  ")
    try:
        your_name = str(your_name)
    except ValueError:
        continue
    else:
        break

while True:
    their_name = input(f"{your_name}, what is target's name?  ")
    try:
        their_name = str(their_name)
    except ValueError:
        continue
    else:
        break

while True:
    state = input(f"{your_name}, what US state or territory are you interested in checking?  ")
    try:
        state = str(state)
    except ValueError:
        continue
    else:
        break

while True:
    their_year_of_birth = input(f"{your_name}, what year was {their_name} born?  ")
    try:
        their_year_of_birth = int(their_year_of_birth)
    except ValueError:
        continue
    else:
        break

while True:
    your_year_of_birth = input(f"{your_name}, what year were you born?  ")
    try:
        your_year_of_birth = int(your_year_of_birth)
    except ValueError:
        continue
    else:
        break

legal_to_consent = {
    'Alabama': 16,
    'Alaska': 16,
    'American Samoa': 16,
    'Arizona': 18,
    'Arkansas': 16,
    'California': 18,
    'Colorado': 17,
    'Connecticut': 16,
    'Delaware': 18,
    'District of Columbia': 16,
    'Florida': 18,
    'Georgia': 16,
    'Guam': 16,
    'Hawaii': 16,
    'Idaho': 18,
    'Illinois': 17,
    'Indiana': 16,
    'Iowa': 16,
    'Kansas': 16,
    'Kentucky': 16,
    'Louisiana': 17,
    'Maine': 16,
    'Maryland': 16,
    'Massachusetts': 16,
    'Michigan': 16,
    'Minnesota': 16,
    'Mississippi': 16,
    'Missouri': 17,
    'Montana': 16,
    'Nebraska': 16,
    'Nevada': 16,
    'New Hampshire': 16,
    'New Jersey': 16,
    'New Mexico': 17,
    'New York': 17,
    'North Carolina': 16,
    'North Dakota': 18,
    'Ohio': 16,
    'Oklahoma': 16,
    'Oregon': 18,
    'Pennsylvania': 16,
    'Puerto Rico': 16,
    'Rhode Island': 16,
    'South Carolina': 16,
    'South Dakota': 16,
    'Tennessee': 18,
    'Texas': 17,
    'US Virgin Islands': 18,
    'Utah': 18,
    'Vermont': 16,
    'Virginia': 18,
    'Washington': 16,
    'West Virginia': 16,
    'Wisconsin': 18,
    'Wyoming': 17,
}

' Milestones to compute '
their_age = date.today().year - their_year_of_birth
your_age = date.today().year - your_year_of_birth
milestones = [5, 10, 16, 18, 21, 22, 24, 25, 50, 75, 100]

' Outcomes '
romeo_and_juliet = f"able to consent in {state} to {your_name} under Romeo & Juliet Laws of {state} since you are roughly {your_age} years old and {their_name} is roughly {their_age} years old"
jail_bait = f"still jail bait until {legal_to_consent.get(state)} years old in {state}"

' Renders results '
if their_year_of_birth + 100 < date.today().year:
    print(f"WOW {your_name}, {their_name} is roughly {their_age} years old!")
elif their_year_of_birth > date.today().year:
    print(f"Congratulations!  {their_name} will be born soon presumably in the year of {their_year_of_birth}!")
elif their_year_of_birth < date.today().year:
    print(f"Since {their_name} is roughly {their_age} years old, thus is ")
    if their_age >= legal_to_consent[state] and your_age >= legal_to_consent[state]:
        print(f"able to freely consent in {state}")
    elif their_age < legal_to_consent[state] or your_age < legal_to_consent[state]:
        if int(your_age) - int(their_age) <= 2 or int(their_age) - int(your_age) <= 2:
            if state == 'Alabama' or state == 'Arizona' or state == 'Connecticut' or state == 'Minnesota' or state == 'Mississippi' or state == 'Washington':
                print(romeo_and_juliet)
            else:
                print(jail_bait)
        elif int(your_age) - int(their_age) <= 3 or int(their_age) - int(your_age) <= 3:
            if state == 'Alaska' or state == 'Arkansas' or state == 'Louisiana' or state == 'Oregon' or state == 'South Dakota' or state == 'Texas':
                print(romeo_and_juliet)
            else:
                print(jail_bait)
        elif int(your_age) - int(their_age) <= 4 or int(their_age) - int(your_age) <= 4:
            if state == 'Colorado' or state == 'Iowa' or state == 'Maryland' or state == 'New Jersey' or state == 'New Mexico' or state == 'North Carolina' or state == 'Pennsylvania' or state == 'Tennessee' or state == 'West Virginia' or state == 'Wyoming':
                print(romeo_and_juliet)
            else:
                print(jail_bait)
        elif int(your_age) - int(their_age) <= 5 or int(their_age) - int(your_age) <= 5:
            if state == 'Hawaii' or state == 'Maine':
                print(romeo_and_juliet)
            else:
                print(jail_bait)
        else:
            print(jail_bait)

for milestone in milestones:
    if their_year_of_birth + milestone > date.today().year:
        print(f"{their_name} will turn {milestone} in {str(their_year_of_birth + milestone)}")
