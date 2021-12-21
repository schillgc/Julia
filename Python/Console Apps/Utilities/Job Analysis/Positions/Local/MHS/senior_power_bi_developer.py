""" Income """
# Job Specific Source
company = "Material Handling Systems"
months = 6
job_title = "Senior Power BI Developer (" + str(months) + " Months Contract-to-Hire)"
pay_rate = 60
gross_job_specific_base_income = pay_rate * (2080 * (months / 12))


''' Monthly Benefits Fixed Expenses '''
medical_insurance = 311.51
dental_insurance = 15.87
vision_insurance = 3.61
monthly_fixed_benefit_expenses = medical_insurance + dental_insurance + vision_insurance


''' Annual Benefits '''
health_savings_account = 3450
voluntary_life_insurance = 110000 / 1000 * 0.15
annual_fixed_benefit_expenses = health_savings_account + voluntary_life_insurance


"""" Taxes """
federal_income_tax = gross_job_specific_base_income * 0.0762
state_income_tax = gross_job_specific_base_income * 0.0517
local_income_tax = gross_job_specific_base_income * 0.0201
income_taxes = federal_income_tax + state_income_tax + local_income_tax

social_security = gross_job_specific_base_income * 0.058
medicare = gross_job_specific_base_income * 0.0136
fica = social_security + medicare

taxes = income_taxes + fica