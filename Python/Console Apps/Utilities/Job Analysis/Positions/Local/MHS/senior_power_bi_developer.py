"""Compensation scenario calculator; sensitive inputs stay in the local environment."""

import os


def _amount(name):
    value = os.environ.get(name, "").strip()
    return float(value) if value else 0.0


company = os.environ.get("JOB_ANALYSIS_EMPLOYER", "Employer")
months = _amount("JOB_ANALYSIS_CONTRACT_MONTHS")
job_title = os.environ.get("JOB_ANALYSIS_ROLE", "Contract role")
pay_rate = _amount("JOB_ANALYSIS_HOURLY_RATE")
gross_job_specific_base_income = pay_rate * (2080 * (months / 12))

monthly_fixed_benefit_expenses = sum(
    _amount(name)
    for name in (
        "JOB_ANALYSIS_MEDICAL_PREMIUM",
        "JOB_ANALYSIS_DENTAL_PREMIUM",
        "JOB_ANALYSIS_VISION_PREMIUM",
    )
)
annual_fixed_benefit_expenses = _amount("JOB_ANALYSIS_HSA_CONTRIBUTION") + _amount(
    "JOB_ANALYSIS_LIFE_INSURANCE_PREMIUM"
)

federal_income_tax = gross_job_specific_base_income * 0.24
state_income_tax = gross_job_specific_base_income * 0.05
local_income_tax = gross_job_specific_base_income * 0.0295
income_taxes = federal_income_tax + state_income_tax + local_income_tax

social_security = gross_job_specific_base_income * 0.062
medicare = gross_job_specific_base_income * 0.0145
fica = social_security + medicare
taxes = income_taxes + fica
