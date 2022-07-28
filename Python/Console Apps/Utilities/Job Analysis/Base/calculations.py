import math

from Base.Expenses.fixed import auto_insurance, child_support, condo_association_fee, gym, home_insurance, hulu, \
    internet, mortgage_payment, reimburse_mama, reimburse_ellie, wroth_ira_contribution
from Base.Expenses.variable import gas, groceries, utilities
from Base.Income.external import cash_on_hand, current_savings

company = input("Company: ")
if company == "StyleSeat":
    from Positions.Local.StyleSeat.senior_data_engineer import annual_fixed_benefit_expenses, \
        gross_job_specific_base_income, job_title, monthly_fixed_benefit_expenses, months, taxes
elif company == "Creative Management Group" or company == "CMG":
    from Positions.Local.CMG.brand_ambassador import annual_fixed_benefit_expenses, \
        gross_job_specific_base_income, job_title, monthly_fixed_benefit_expenses, months, taxes
elif company == "HCL Technologies" or company == "HCL":
    from Positions.OutOfTown.HCL.python_developer import annual_fixed_benefit_expenses, \
        gross_job_specific_base_income, job_title, monthly_fixed_benefit_expenses, months, taxes
elif company == "Lexmark International, Inc." or company == "Lexmark" or company == "LII":
    from Positions.OutOfTown.LII.full_stack_software_engineer import annual_fixed_benefit_expenses, \
        gross_job_specific_base_income, job_title, monthly_fixed_benefit_expenses, months, taxes
elif company == "Material Handling Systems" or company == "MHS":
    from Positions.Local.MHS.senior_power_bi_developer import annual_fixed_benefit_expenses, \
        gross_job_specific_base_income, job_title, monthly_fixed_benefit_expenses, months, taxes
elif company == "Stock Yards Bank" or company == "SYB":
    from Positions.Local.StockYardsBank.web_developer import annual_fixed_benefit_expenses, \
        gross_job_specific_base_income, job_title, monthly_fixed_benefit_expenses, months, taxes
elif company == "TATA Consultantancy Services" or company == "TCS":
    from Positions.OutOfTown.TCS.data_scientist import annual_fixed_benefit_expenses, \
        gross_job_specific_base_income, job_title, monthly_fixed_benefit_expenses, months, taxes
elif company == "Technical Consulting Inc" or company == "TCI":
    from Positions.Local.TCI.automation_developer import annual_fixed_benefit_expenses, \
        gross_job_specific_base_income, job_title, monthly_fixed_benefit_expenses, months, taxes
else:
    annual_fixed_benefit_expenses = 0
    gross_job_specific_base_income = 0
    job_title = "Freelance"
    monthly_fixed_benefit_expenses = 0
    months = 12
    taxes = 0

duration = months
jobtitle = job_title
wages = gross_job_specific_base_income

""" Income """
external_revenue_sources = cash_on_hand + current_savings
adjusted_gross_income = external_revenue_sources + gross_job_specific_base_income

""" Expenses """
# Private Fixed Expenses
# Monthly
monthly_private_fixed_expenses = auto_insurance + child_support + condo_association_fee + gym + home_insurance + hulu + \
                                 internet + mortgage_payment

# Annual
annual_private_fixed_expenses = wroth_ira_contribution

# Subtotal Private Fixed Expenses
subtotal_private_fixed_expenses = (annual_private_fixed_expenses * math.ceil(months / 12)) + \
                                  (monthly_private_fixed_expenses * months)

# Benefits Fixed Expenses
# Subtotal Benefits Fixed Expenses
subtotal_benefits_fixed_expenses = (annual_fixed_benefit_expenses * math.ceil(months / 12)) + \
                                   (monthly_fixed_benefit_expenses * months)

# Variable Expenses
# Monthly
monthly_variable_expenses = gas + groceries + utilities

# One-Time Expenses
total_one_time_major_expenses = reimburse_mama + reimburse_ellie

# Expense Totals
total_fixed_expenses = subtotal_benefits_fixed_expenses + subtotal_private_fixed_expenses
total_calculated_expenses = (monthly_variable_expenses * months) + total_fixed_expenses + total_one_time_major_expenses \
                            + taxes
total_monthly_expenses = monthly_fixed_benefit_expenses + monthly_private_fixed_expenses + monthly_variable_expenses

""" Assets """
emergency_savings = total_monthly_expenses * 3
profits = adjusted_gross_income - total_calculated_expenses

"""Recalculations"""
total_one_time_major_expenses += emergency_savings
