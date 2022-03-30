""" Income """
# Job Specific Source
company = "HCL"
months = 12
job_title = "Python Developer (Direct Hire -- Charlotte, NC)"
pay_rate = 120000 / 2080
gross_job_specific_base_income = pay_rate * (2080 * (months / 12))


''' Monthly Benefits Fixed Expenses '''
medical_insurance = 82
dental_insurance = 8.5
vision_insurance = 11.12
monthly_fixed_benefit_expenses = medical_insurance + dental_insurance + vision_insurance


''' Annual Benefits '''
flex_spending_account = 2650 # Bank of America
retirement_401K = gross_job_specific_base_income * .05
annual_fixed_benefit_expenses = flex_spending_account + retirement_401K


"""" Taxes """
federal_income_tax = gross_job_specific_base_income * 0.03
state_income_tax = gross_job_specific_base_income * ((10/3) / 100)
local_income_tax = gross_job_specific_base_income * 0
income_taxes = federal_income_tax + state_income_tax + local_income_tax

social_security = gross_job_specific_base_income * 0.0449
medicare = gross_job_specific_base_income * 0.0105
fica = social_security + medicare

taxes = income_taxes + fica
