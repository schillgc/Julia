""" Income """
# Job Specific Source
company = "LII"
months = 12
job_title = "Full-Stack Software Engineer (Direct Hire -- REMOTE & Lexington, KY)"
pay_rate = 180000 / 2080
gross_job_specific_base_income = pay_rate * (2080 * (months / 12))


''' Monthly Benefits Fixed Expenses '''
medical_insurance = 0
dental_insurance = 0
vision_insurance = 0
monthly_fixed_benefit_expenses = medical_insurance + dental_insurance + vision_insurance


''' Annual Benefits '''
flex_spending_account = 0
retirement_401K = gross_job_specific_base_income * .00
annual_fixed_benefit_expenses = flex_spending_account + retirement_401K


"""" Taxes """
federal_income_tax = gross_job_specific_base_income * 0.32
state_income_tax = gross_job_specific_base_income * 0.05
local_income_tax = gross_job_specific_base_income * 0.0225
income_taxes = federal_income_tax + state_income_tax + local_income_tax

social_security = gross_job_specific_base_income * 0.062
medicare = gross_job_specific_base_income * 0.0145
fica = social_security + medicare

taxes = income_taxes + fica
