from financials.assets import annualSalary, dailyPay, hourlyPay, hsaAnnualLimit, monthlySalary, numberOfAnnualWorkWeeks, \
    numberOfDailyWorkHours, numberOfWeeklyWorkDays, rothIRAAnnualLimit, snapMonthlyBenefits, weeklySalary
from financials.expenses import amazonChaseBankCreditCardBalance, childSupportMonthly, dentalInsuranceWeeklyPremium, \
    epaEstimatedWeeklyGasConsumptionCost, freedomMortgageMonthlyPayment, healthInsuranceWeeklyPremium, \
    hertzMonthlyCarRental, hoaMonthly, hoaPaidInFullDiscount, loanBalanceToEllie, loanBalanceToMama, \
    sprintMonthly, visionInsuranceWeeklyPremium
from financials.taxes import federalTaxPercentage, localTaxPercentage, medicarePercentage, socialSecurityPercentage, \
    stateTaxPercentage, taxFederal, taxLocal, taxState

frequency = input("What pay frequency do you want to figure (Annually | Monthly | Weekly | Daily | Hourly | Per "
                  "Minute)? ")
print(frequency, "Report\n")

timeFrequencyDivider = 0
if frequency == "Annually":
    frequency = annualSalary
    timeFrequencyDivider = 1
elif frequency == "Monthly":
    frequency = monthlySalary
    timeFrequencyDivider = 12
elif frequency == "Weekly":
    frequency = weeklySalary
    timeFrequencyDivider = numberOfAnnualWorkWeeks
elif frequency == "Daily":
    frequency = dailyPay
    timeFrequencyDivider = numberOfAnnualWorkWeeks * numberOfWeeklyWorkDays
elif frequency == "Hourly":
    frequency = hourlyPay
    timeFrequencyDivider = numberOfAnnualWorkWeeks * numberOfWeeklyWorkDays * numberOfDailyWorkHours
elif frequency == "Per Minute":
    frequency = hourlyPay
    timeFrequencyDivider = numberOfAnnualWorkWeeks * numberOfWeeklyWorkDays * numberOfDailyWorkHours * 60

assets = {"Health Savings Account:": '${:,.2f}'.format(hsaAnnualLimit / timeFrequencyDivider),
          "Roth IRA": '${:,.2f}'.format(rothIRAAnnualLimit / timeFrequencyDivider),
          "SNAP": '${:,.2f}'.format(snapMonthlyBenefits * 12 / timeFrequencyDivider),
          "Salary": '${:,.2f}'.format(annualSalary / timeFrequencyDivider)}
print("Assets:", assets)

taxes = {"Medicare:": '${:,.2f}'.format(frequency * medicarePercentage),
         "Social Security": '${:,.2f}'.format(frequency * socialSecurityPercentage),
         taxLocal: '${:,.2f}'.format(frequency * localTaxPercentage),
         taxState: '${:,.2f}'.format(frequency * stateTaxPercentage),
         taxFederal: '${:,.2f}'.format(frequency * federalTaxPercentage)}
print("Taxes:", taxes)

debt = {"Amazon | Chase Bank": '${:,.2f}'.format(amazonChaseBankCreditCardBalance / timeFrequencyDivider),
        "Ellie": '${:,.2f}'.format(loanBalanceToEllie / timeFrequencyDivider),
        "Mama": '${:,.2f}'.format(loanBalanceToMama / timeFrequencyDivider)}
print("Debt:", debt)

flexExpenses = {"Gas": '${:,.2f}'.format(epaEstimatedWeeklyGasConsumptionCost * 52 / timeFrequencyDivider)}
print("Flex Expenses:", flexExpenses)

fixedExpenses = {
    "Anthem Health Insurance": '${:,.2f}'.format(healthInsuranceWeeklyPremium * 52 / timeFrequencyDivider),
    "Freedom Mortgage": '${:,.2f}'.format(freedomMortgageMonthlyPayment * 12 / timeFrequencyDivider),
    "Guardian Dental Insurance": '${:,.2f}'.format(dentalInsuranceWeeklyPremium * 52 / timeFrequencyDivider),
    "Guardian Vision Insurance": '${:,.2f}'.format(visionInsuranceWeeklyPremium * 52 / timeFrequencyDivider),
    "Hayden's Child Support": '${:,.2f}'.format(childSupportMonthly * 12 / timeFrequencyDivider),
    "Hertz Car Rental": '${:,.2f}'.format(hertzMonthlyCarRental * 12 / timeFrequencyDivider),
    "Parkview Condo HOA": '${:,.2f}'.format(hoaPaidInFullDiscount * hoaMonthly * 12 / timeFrequencyDivider),
    "Sprint": '${:,.2f}'.format(sprintMonthly * 12 / timeFrequencyDivider)}
print("Fixed Expenses:", fixedExpenses)
