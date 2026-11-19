"""Budget inputs. Personal amounts are supplied locally, never committed."""

import os


def _amount(name):
    value = os.environ.get(name, "").strip()
    return float(value) if value else 0.0


hsaAnnualLimit = _amount("BUDGET_HSA_ANNUAL_LIMIT")
rothIRAAnnualLimit = _amount("BUDGET_ROTH_IRA_ANNUAL_LIMIT")
snapMonthlyBenefits = _amount("BUDGET_MONTHLY_ASSISTANCE")
annualSalary = _amount("BUDGET_ANNUAL_INCOME")
numberOfDailyWorkHours = _amount("BUDGET_DAILY_WORK_HOURS") or 6
numberOfWeeklyWorkDays = _amount("BUDGET_WEEKLY_WORK_DAYS") or 5
numberOfAnnualWorkWeeks = _amount("BUDGET_ANNUAL_WORK_WEEKS") or 47

weeklySalary = annualSalary / numberOfAnnualWorkWeeks
dailyPay = weeklySalary / numberOfWeeklyWorkDays
hourlyPay = dailyPay / numberOfDailyWorkHours
monthlySalary = annualSalary / 12
