"""Budget expense inputs loaded from local environment variables."""

import os


def _amount(name):
    value = os.environ.get(name, "").strip()
    return float(value) if value else 0.0


amazonChaseBankCreditCardBalance = _amount("BUDGET_CREDIT_CARD_BALANCE")
familyLoanOneBalance = _amount("BUDGET_FAMILY_LOAN_ONE_BALANCE")
familyLoanTwoBalance = _amount("BUDGET_FAMILY_LOAN_TWO_BALANCE")
epaEstimatedWeeklyGasConsumptionCost = _amount("BUDGET_WEEKLY_FUEL_COST")
healthInsuranceWeeklyPremium = _amount("BUDGET_WEEKLY_HEALTH_PREMIUM")
freedomMortgageMonthlyPayment = _amount("BUDGET_MONTHLY_HOUSING_PAYMENT")
dentalInsuranceWeeklyPremium = _amount("BUDGET_WEEKLY_DENTAL_PREMIUM")
visionInsuranceWeeklyPremium = _amount("BUDGET_WEEKLY_VISION_PREMIUM")
childSupportMonthly = _amount("BUDGET_MONTHLY_CHILD_SUPPORT")
hertzMonthlyCarRental = _amount("BUDGET_MONTHLY_TRANSPORTATION")
hoaMonthly = _amount("BUDGET_MONTHLY_ASSOCIATION_FEE")

hoaPaidInFullDiscount = os.environ.get(
    "BUDGET_HOA_PAID_IN_FULL_DISCOUNT", "false"
).strip().lower() in {"1", "true", "yes", "on"}
hoaPaidInFullDiscount = 0.9 if hoaPaidInFullDiscount else 1.0

sprintMonthly = _amount("BUDGET_MONTHLY_PHONE")
