import locale

try:
    locale.setlocale(locale.LC_ALL, 'English_United States.1252')
except:
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

family = ["Blair", "Ellie", "Gavin", "Hayden", "Ian", "Rusti"]

primary_phone_line = 73
secondary_phone_line = 50
additional_phone_line = 30
additional_lines = len(family) - 2
taxes_and_fees = 6.76

total_phone_line_cost = primary_phone_line + secondary_phone_line + (
            additional_phone_line * additional_lines)
print("Total Phone Line Cost:", locale.currency(total_phone_line_cost, grouping=True))

divided_base_phone_plan_charge = total_phone_line_cost / (len(family))
print("Divided Phone Line Charge:", locale.currency(divided_base_phone_plan_charge, grouping=True))
