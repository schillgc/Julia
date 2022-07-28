""" Income """
# Job Specific Source
company = "Creative Management Group"
months = 1
job_title = "Brand Ambassador (" + str(months) + " Month)"
pay_rate = 28
gross_job_specific_base_income = pay_rate * (2080 * (months / 12))


''' Monthly Benefits Fixed Expenses '''
medical_insurance = 0
dental_insurance = 0
vision_insurance = 0
monthly_fixed_benefit_expenses = medical_insurance + dental_insurance + vision_insurance


''' Annual Benefits '''
health_savings_account = 0
voluntary_life_insurance = 0
annual_fixed_benefit_expenses = health_savings_account + voluntary_life_insurance


"""" Taxes """
federal_income_tax = gross_job_specific_base_income * 0.22
state_income_tax = gross_job_specific_base_income * 0.05
local_income_tax = gross_job_specific_base_income * 0.0295
income_taxes = federal_income_tax + state_income_tax + local_income_tax

social_security = gross_job_specific_base_income * 0.062
medicare = gross_job_specific_base_income * 0.0145
fica = social_security + medicare

taxes = income_taxes + fica