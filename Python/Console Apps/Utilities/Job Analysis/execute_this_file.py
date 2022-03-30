#!/usr/bin/env python3
import locale

from Base.Income.external import cash_on_hand, current_savings
from Base.calculations import company, duration, emergency_savings, external_revenue_sources, jobtitle, profits,\
    total_calculated_expenses, wages

# Sets currency type by locale
locale.setlocale(locale.LC_ALL, 'en_US')


'''Balance Sheet'''
print(company, "-", jobtitle)
print(duration, "Months Gross Income:", locale.currency(wages, grouping=True))
print("Current Savings:", locale.currency(current_savings, grouping=True))
print("Cash On Hand:", locale.currency(cash_on_hand, grouping=True))
print("Profits:", locale.currency(profits, grouping=True))
print("Emergency Savings:", locale.currency(emergency_savings, grouping=True))
print("Adjusted Disposable Income:", locale.currency(profits - emergency_savings, grouping=True))
print("Monthly Adjusted Disposable Income:", locale.currency((profits - emergency_savings) / duration, grouping=True))
print("Break-Even Rate:", locale.currency(((total_calculated_expenses + emergency_savings - external_revenue_sources) /
                                           duration) / (4 + (1 / 3)) / 40, grouping=True),
    "per hour before remaining mortgage balance")
