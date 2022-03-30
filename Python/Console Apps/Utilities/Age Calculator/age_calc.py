from legal import drivers_license, drinking,consent, permit
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

' Milestones to compute '
their_age = date.today().year - their_year_of_birth
your_age = date.today().year - your_year_of_birth
milestones = [5, 10, permit[state], drivers_license[state], consent[state], drinking, 22, 24, 25, 50, 75, 100]

' Outcomes '
romeo_and_juliet = f"able to consent in {state} to {your_name} under Romeo & Juliet Laws of {state} since {your_name} is roughly {your_age} years old and {their_name} is roughly {their_age} years old"
jail_bait = f"still jail bait until {consent.get(state)} years old in {state}"

' Renders results '
if their_year_of_birth + 100 < date.today().year:
    print(f"WOW {your_name}, {their_name} is roughly {their_age} years old!")
elif their_year_of_birth > date.today().year:
    print(f"Congratulations!  {their_name} will be born soon presumably in {their_year_of_birth}!")
elif their_year_of_birth == date.today().year:
    print(f"{their_name} is busy fucking their way out of their Mama this year, {your_name}!")
elif their_year_of_birth < date.today().year:
    print(f"Since {their_name} is roughly {their_age} years old, thus is ")
    if their_age >= consent[state] and your_age >= consent[state]:
        print(f"able to freely consent in {state}")
    elif their_age < consent[state] or your_age < consent[state]:
        if state == 'Alabama' or state == 'Arizona' or state == 'Connecticut' or state == 'Minnesota' or state == 'Mississippi' or state == 'Washington':
            if int(your_age) - int(their_age) <= 2 and int(their_age) - int(your_age) <= 2 and consent[state] - int(your_age) <= 2 and consent[state] - int(their_age) <= 2:
                print(romeo_and_juliet)
            else:
                print(jail_bait)
        elif state == 'Alaska' or state == 'Arkansas' or state == 'Louisiana' or state == 'Oregon' or state == 'South Dakota' or state == 'Texas':
            if int(your_age) - int(their_age) <= 3 and int(their_age) - int(your_age) <= 3 and consent[state] - int(your_age) <= 3 and consent[state] - int(their_age) <= 3:
                print(romeo_and_juliet)
            else:
                print(jail_bait)
        elif state == 'Colorado' or state == 'Iowa' or state == 'Maryland' or state == 'New Jersey' or state == 'New Mexico' or state == 'North Carolina' or state == 'Pennsylvania' or state == 'Tennessee' or state == 'West Virginia' or state == 'Wyoming':
            if int(your_age) - int(their_age) <= 4 and int(their_age) - int(your_age) <= 4 and consent[state] - int(your_age) <= 4 and consent[state] - int(their_age) <= 4:
                print(romeo_and_juliet)
            else:
                print(jail_bait)
        elif state == 'Hawaii' or state == 'Maine':
            if int(your_age) - int(their_age) <= 5 and int(their_age) - int(your_age) <= 5 and consent[state] - int(your_age) <= 5 and consent[state] - int(their_age) <= 5:
                print(romeo_and_juliet)
            else:
                print(jail_bait)
        else:
            print(jail_bait, "as", state, "does not have any known Romeo & Juliet Laws at this time.  You may want to double check.")

for milestone in milestones:
    if their_year_of_birth + milestone > date.today().year:
        if milestone == permit[state]:
            print(f"Care to take a drive with me, {their_name} as soon as permitted by {state} in {str(their_year_of_birth + milestone)}?")
        elif milestone == drivers_license[state]:
            print(f"{their_name} can be designed driver as soon as licensed by {state} in {str(their_year_of_birth + milestone)}")
        elif milestone == consent[state]:
            print(f"Fuck yeah, {their_name} in {state} in {str(their_year_of_birth + milestone)}!")
        elif milestone == drinking:
            print(f"Party on in the USA, {their_name} in {str(their_year_of_birth + milestone)}!")
        elif milestone == 100:
            print(f"{their_name} will become an antique in {str(their_year_of_birth + milestone)}")
        else:
            print(f"{their_name} will turn {milestone} in {str(their_year_of_birth + milestone)}")

print(date.today())
