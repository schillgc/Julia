""" HSA """
hsaAnnualLimit = 3450

""" Roth IRA """
rothIRAAnnualLimit = 5500

""" SNAP """
snapMonthlyBenefits = 357

""" Salary """
annualSalary = 92000
numberOfDailyWorkHours = 6
numberOfWeeklyWorkDays = 5
numberOfAnnualWorkWeeks = 47

weeklySalary = annualSalary / numberOfAnnualWorkWeeks
dailyPay = weeklySalary / numberOfWeeklyWorkDays
hourlyPay = dailyPay / numberOfDailyWorkHours
monthlySalary = annualSalary / 12

""" Report """