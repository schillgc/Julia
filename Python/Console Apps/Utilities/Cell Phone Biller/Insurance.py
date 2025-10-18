import locale
from datetime import date

try:
    locale.setlocale(locale.LC_ALL, 'English_United States.1252')
except:
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

family = ["Blair", "Ellie", "Gavin", "Hayden", "Ian", "Rusti"]
number_of_lines = len(family)

for family_member in family:
    sprint_complete = 0
    protection_plan_for_hayden = True
    if protection_plan_for_hayden:
        if family_member not in ["Hayden", "Ian"]:
            # Hayden's Protection Plan
            sprint_complete += (7 / (number_of_lines - 2))
    if family_member != "Hayden":
        sprint_complete += 18
    elif date.today() < date(2022, 8, 26) and family_member == "Mama":
        sprint_complete += 15.6
    if sprint_complete != 0:
        print("Sprint Complete for", family_member, ":", locale.currency(
            sprint_complete, grouping=True))
