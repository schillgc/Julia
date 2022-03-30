""" Income """
# Job Specific Source
company = "TATA Consultantancy Services"
months = 12
job_title = "Data Scientist (Direct Hire -- Bradenton, FL)"
pay_rate = 110000 / 2080
gross_job_specific_base_income = pay_rate * (2080 * (months / 12))


''' Monthly Benefits Fixed Expenses '''
medical_insurance = 110
dental_insurance = 10.65
vision_insurance = 2.65
monthly_fixed_benefit_expenses = medical_insurance + dental_insurance + vision_insurance


''' Annual Benefits '''
flex_spending_account = 2650
retirement_401K = gross_job_specific_base_income * .05
annual_fixed_benefit_expenses = flex_spending_account + retirement_401K


"""" Taxes """
federal_income_tax = gross_job_specific_base_income * 0.0626
state_income_tax = gross_job_specific_base_income * 0
local_income_tax = gross_job_specific_base_income * 0
income_taxes = federal_income_tax + state_income_tax + local_income_tax

social_security = gross_job_specific_base_income * 0.059
medicare = gross_job_specific_base_income * 0.0138
fica = social_security + medicare

taxes = income_taxes + fica
