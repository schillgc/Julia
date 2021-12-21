annualSalary = 92000
numberOfDailyWorkHours = 6
numberOfWeeklyWorkDays = 5
numberOfAnnualWorkWeeks = 47
monthlySalary = annualSalary / 12
weeklySalary = annualSalary / numberOfAnnualWorkWeeks
dailyPay = weeklySalary / numberOfWeeklyWorkDays
hourlyPay = dailyPay / numberOfDailyWorkHours

taxFederal = "United States of America"
taxState = "Kentucky"
taxLocal = "Louisville"
federalTaxPercentage = .0145
stateTaxPercentage = .0458
localTaxPercentage = .0182
socialSecurityPercentage = .053
medicarePercentage = .0124

loanBalanceToMama = 12000
amazonChaseBankCreditCardBalance = 2000

hoaMonthly = 254
hoaPaidInFullDiscount = True
childSupportMonthly = 277
healthInsuranceWeeklyPremium = 180.56
dentalInsuranceWeeklyPremium = 8.99
visionInsuranceWeeklyPremium = 1.578
sprintMonthly = 65
hertzMonthlyCarRental = 445
freedomMortgageMonthlyPayment = 336

epaEstimatedWeeklyGasConsumptionCost = 85.65
snapMonthlyBenefits = 357

rothIRAAnnualLimit = 5500
hsaAnnualLimit = 3450

if hoaPaidInFullDiscount:
    hoaPaidInFullDiscount = .9
else:
    hoaPaidInFullDiscount = 1

frequency = input("What pay frequency do you want to figure (Annually | Monthly | Weekly | Daily | Hourly | Per Minute)? ")
print(frequency, "Report")

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

assets = {"Roth IRA": '${:,.2f}'.format(rothIRAAnnualLimit / timeFrequencyDivider),
          "HSA:": '${:,.2f}'.format(hsaAnnualLimit / timeFrequencyDivider)}
print("Assets:", assets)

taxes = {taxFederal: '${:,.2f}'.format(frequency * federalTaxPercentage),
         taxState: '${:,.2f}'.format(frequency * stateTaxPercentage),
         taxLocal: '${:,.2f}'.format(frequency * localTaxPercentage),
         "Social Security": '${:,.2f}'.format(frequency * socialSecurityPercentage),
         "Medicare:": '${:,.2f}'.format(frequency * medicarePercentage)}
print("Taxes:", taxes)

debt = {"Mama": '${:,.2f}'.format(loanBalanceToMama / timeFrequencyDivider),
        "Amazon | Chase Bank": '${:,.2f}'.format(amazonChaseBankCreditCardBalance / timeFrequencyDivider)}
print("Debt:", debt)

flexExpenses = {"Gas": '${:,.2f}'.format(epaEstimatedWeeklyGasConsumptionCost * 52 / timeFrequencyDivider),
                "Food": '${:,.2f}'.format(snapMonthlyBenefits * 12 / timeFrequencyDivider)}
print("Flex Expenses:", flexExpenses)

fixedExpenses = {
    "Parkview Condo HOA": '${:,.2f}'.format(hoaPaidInFullDiscount * hoaMonthly * 12 / timeFrequencyDivider),
    "Hayden's Child Support": '${:,.2f}'.format(childSupportMonthly * 12 / timeFrequencyDivider),
    "Anthem Health Insurance": '${:,.2f}'.format(healthInsuranceWeeklyPremium * 52 / timeFrequencyDivider),
    "Guardian Dental Insurance": '${:,.2f}'.format(dentalInsuranceWeeklyPremium * 52 / timeFrequencyDivider),
    "Guardian Vision Insurance": '${:,.2f}'.format(visionInsuranceWeeklyPremium * 52 / timeFrequencyDivider),
    "Sprint": '${:,.2f}'.format(sprintMonthly * 12 / timeFrequencyDivider),
    "Hertz Car Rental": '${:,.2f}'.format(hertzMonthlyCarRental * 12 / timeFrequencyDivider),
    "Freedom Mortgage": '${:,.2f}'.format(freedomMortgageMonthlyPayment * 12 / timeFrequencyDivider)}
print("Fixed Expenses:", fixedExpenses)
