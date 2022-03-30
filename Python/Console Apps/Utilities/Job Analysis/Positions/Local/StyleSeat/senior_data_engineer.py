from Base.Expenses.fixed import gym, hulu, internet

""" Income """
# Job Specific Source
company = "StyleSeat"
job_title = "Remote - Senior Data Engineer (Direct Hire)"
pay_rate = 200000 / 2080
months = 12

gross_job_specific_base_income = pay_rate * (2080 * (months / 12))

if gym > 0:
    if gym >= 75:
        gym = gym - 75
    else:
        gym = 0

if hulu > 0:
    if hulu >= 9.99:
        hulu = hulu - 9.99
    else:
        hulu = 0

if internet > 0:
    if internet >= 35:
        internet = internet - 35
    else:
        internet = 0


""" Expenses """
# Monthly Benefits Fixed Expenses
medical_insurance = 23.40
dental_insurance = 0.00
vision_insurance = 0.00

monthly_fixed_benefit_expenses = medical_insurance + dental_insurance + vision_insurance


# Annual Benefits Fixed Expenses
retirement_401K = pay_rate * 0.06
annual_fixed_benefit_expenses = retirement_401K


"""" Taxes """
federal_income_tax = gross_job_specific_base_income * 0
state_income_tax = gross_job_specific_base_income * 0.0371
local_income_tax = gross_job_specific_base_income * 0.0154
income_taxes = federal_income_tax + state_income_tax + local_income_tax

social_security = gross_job_specific_base_income * 0.0559
medicare = gross_job_specific_base_income * 0.0131
fica = social_security + medicare

taxes = income_taxes + fica
