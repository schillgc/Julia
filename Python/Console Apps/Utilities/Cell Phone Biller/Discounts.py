from datetime import date
import locale

locale.setlocale(locale.LC_ALL, 'English_United States.1252')
family = ["Blair", "Ellie", "Gavin", "Hayden", "Ian", "Rusti"]

for family_member in family:
    discounts = 0

    apple_trade_in = True
    auto_pay = True
    auto_pay_plan_discount = 5
    if auto_pay:
        discounts += auto_pay_plan_discount
    else:
        print("You can save by auto-paying")

    if family_member == "Gavin":
        sprint_perks_discount = 5
        discounts += sprint_perks_discount
    elif family_member == "Hayden":
        line_on_us_three_unlimited_service_plan = 25
        discounts += line_on_us_three_unlimited_service_plan
    elif family_member == "Rusti" and date.today() < date(2024, 7, 31) and apple_trade_in:
        discounts += 16.67
    elif family_member == "Ian" and date.today() < date(2024, 4, 30) and apple_trade_in:
        discounts += 25

    if not discounts == 0:
        print("Discounts for", family_member, ":", locale.currency(discounts, grouping=True))

# Gavin's $ 51.95
# Hayden's Free
# Ian's $ 65.29
# Ellie's $ 59.45
# Blair's $ 59.45
# Rusti's $ 91.72
