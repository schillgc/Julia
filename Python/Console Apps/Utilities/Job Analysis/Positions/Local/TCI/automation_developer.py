""" Income """
# Job Specific Source
company = "Technology Consulting Inc."
job_title = "Automation Developer (LG&E)"
pay_rate = 110000 / 2080
months = 12

gross_job_specific_base_income = pay_rate * (2080 * (months / 12))

""" Expenses """
# Monthly Benefits Fixed Expenses
medical_insurance = 148.54 * 2
dental_insurance = 12.15 * 2
vision_insurance = 3.78 * 2

monthly_fixed_benefit_expenses = medical_insurance + dental_insurance + vision_insurance

# Annual Benefits Fixed Expenses
retirement_401K = pay_rate * 0

annual_fixed_benefit_expenses = retirement_401K

"""" Taxes """
federal_income_tax = gross_job_specific_base_income * 0.24
state_income_tax = gross_job_specific_base_income * 0.05
local_income_tax = gross_job_specific_base_income * 0.0295
income_taxes = federal_income_tax + state_income_tax + local_income_tax

social_security = gross_job_specific_base_income * 0.062
medicare = gross_job_specific_base_income * 0.0145
fica = social_security + medicare

taxes = income_taxes + fica
