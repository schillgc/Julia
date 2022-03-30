""" Income """
# Job Specific Source
company = "Stock Yards Bank"
job_title = "Web Developer (Direct Hire)"
pay_rate = 60000 / 2080
months = 12

gross_job_specific_base_income = pay_rate * (2080 * (months / 12))

""" Expenses """
# Monthly Benefits Fixed Expenses
medical_insurance = 102.5 * 2
dental_insurance = 13.9 * 2
vision_insurance = 4.01 * 2
voluntary_life_insurance = 150000 / 1000 * 0.0505 * 2
disease_policy = 10.9 * 2
accident_policy = 5.05 * 2
employee_stock_purchase_plan = 5 * 2
flex_qualified_transportation_account = 255

monthly_fixed_benefit_expenses = medical_insurance + dental_insurance + vision_insurance + voluntary_life_insurance + disease_policy + accident_policy + employee_stock_purchase_plan + flex_qualified_transportation_account


# Annual Benefits Fixed Expenses
flex_spending_account = 2650
retirement_401K = pay_rate * 0.06

annual_fixed_benefit_expenses = flex_spending_account + retirement_401K


"""" Taxes """
federal_income_tax = gross_job_specific_base_income * 0
state_income_tax = gross_job_specific_base_income * 0.0371
local_income_tax = gross_job_specific_base_income * 0.0154
income_taxes = federal_income_tax + state_income_tax + local_income_tax

social_security = gross_job_specific_base_income * 0.0559
medicare = gross_job_specific_base_income * 0.0131
fica = social_security + medicare

taxes = income_taxes + fica
