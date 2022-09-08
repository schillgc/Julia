from datetime import date
import locale
locale.setlocale(locale.LC_ALL, 'English_United States.1252')

family = ["Blair", "Ellie", "Gavin", "Hayden", "Ian", "Rusti"]
for family_member in family:
    equipment = 0
    samsung_a11_lease = True
    apple_iphone_13_lease = True

    if date.today() < date(2022, 12, 31) and samsung_a11_lease:
        if family_member == "Rusti" or family_member == "Ellie" or family_member == "Blair":
            equipment += 7.50 / 3  # Hayden's Cell Phone
    if date.today() < date(2024, 7, 31) and apple_iphone_13_lease:
        if family_member == "Rusti":
            equipment += 33.34
    if date.today() < date(2024, 4, 30) and apple_iphone_13_lease:
        if family_member == "Ian":
            equipment += 33.34

    if not equipment == 0:
        print("Equipment for", family_member, ":", locale.currency(equipment, grouping=True))