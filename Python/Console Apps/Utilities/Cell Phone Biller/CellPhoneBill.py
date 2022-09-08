import locale
from datetime import date

locale.setlocale(locale.LC_ALL, 'English_United States.1252')


def bill_ingredients(family_member):
    """ Cell Phone Plan Rates Subtotal """
    number_of_lines = len(family_members)
    line_one = 73
    line_two = 50
    line_for_hayden = 30
    additional_lines = line_for_hayden * (number_of_lines - 3)
    unlimited_basic_phone_plan: float = (
            line_one + line_two + line_for_hayden + additional_lines)
    equally_divided_base_phone_plan_charge = unlimited_basic_phone_plan / (number_of_lines - 1) \
        # does not include Hayden
    print("Equally Divided Plan:", locale.currency(equally_divided_base_phone_plan_charge, grouping=True))

    ''' Auto-Payment & Other Discounts '''
    discounts = 0
    auto_pay = True
    auto_pay_plan_discount = 5
    if auto_pay:
        discounts += auto_pay_plan_discount
    else:
        print("You can save by auto-paying")

    if family_member == "Gavin":
        sprint_perks_discount = 5
        discounts += sprint_perks_discount
    elif family_member == "Hayden":
        line_on_us_three_unlimited_service_plan = 25
        discounts += line_on_us_three_unlimited_service_plan
    elif family_member == "Mama" and date.today() < date(2024, 7, 31):
        discounts += 16.67
    elif family_member == "Ian" and date.today() < date(2024, 4, 30):
        discounts += 25

    if not discounts == 0:
        print("Discounts:", locale.currency(discounts, grouping=True))

    ''' Plans & Services Subtotal '''
    plans_and_services = equally_divided_base_phone_plan_charge - discounts
    if not family_member == "Hayden":
        if (equally_divided_base_phone_plan_charge - line_for_hayden) > 0:
            plans_and_services += (equally_divided_base_phone_plan_charge - line_for_hayden) / (number_of_lines - 1)
        print("Plans & Services (After Discounts):", locale.currency(plans_and_services, grouping=True))

    ''' Hayden's Phone Payoff '''
    equipment = 0
    samsung_a11_lease = True
    apple_iphone_13_lease = True
    if date.today() < date(2022, 12, 31) and samsung_a11_lease:
        if family_member == "Mama" or family_member == "Ellie" or family_member == "Blair":
            equipment += 7.50 / 3  # Hayden's Cell Phone
    if date.today() < date(2024, 4, 30) and apple_iphone_13_lease:
        if family_member == "Ian":
            equipment += 33.34
    if date.today() < date(2024, 7, 31) and apple_iphone_13_lease:
        if family_member == "Mama":
            equipment += 33.34
    if not equipment == 0:
        print("Equipment:", locale.currency(equipment, grouping=True))

    ''' Sprint Complete & Sprint Premium Services Subtotal '''
    sprint_complete = 0
    sprint_premium_services = 0
    protection_plan_for_hayden = True
    if protection_plan_for_hayden:
        if not family_member == "Hayden" and not family_member == "Ian":
            # Hayden's Protection Plan
            sprint_complete += (7 / (number_of_lines - 2))
    if not family_member == "Hayden":
        sprint_complete += 18
    elif date.today() < date(2022, 8, 26) and family_member == "Mama":
        sprint_complete += 15.6
    if not sprint_complete == 0:
        print("Sprint Complete:", locale.currency(
            sprint_complete, grouping=True))
    if not sprint_premium_services == 0:
        print("Sprint Premium Services:", locale.currency(
            sprint_premium_services, grouping=True))

    ''' Surcharges Subtotal '''
    surcharges = 0
    if not family_member == "Hayden":
        administrative_charge = 0
        federal_universal_service_access = 0
        kentucky_state_gross_receipts_surcharge = 0.26
        regulatory_charge = 0
        surcharges += (administrative_charge + federal_universal_service_access +
                       kentucky_state_gross_receipts_surcharge + regulatory_charge) / (number_of_lines - 1)
    if not surcharges == 0:
        print("Surcharges:", locale.currency(surcharges, grouping=True))

    ''' Government Taxes & Fees Subtotal '''
    government_taxes_and_fees = 0
    sales_tax = 0

    if not family_member == "Hayden":
        emergency_tax = 4.2
        lifeline_fee = 0.90
        sales_tax += 0.73
        trs_tap = 0.18
        government_taxes_and_fees += (emergency_tax + lifeline_fee +
                                      sales_tax + trs_tap) / (number_of_lines - 1)

        if family_member == "Mama" and date.today() < date(2022, 8, 26):
            sales_tax += 6.76
            government_taxes_and_fees += sales_tax

    if not government_taxes_and_fees == 0:
        print("Government Taxes & Fees:", locale.currency(
            government_taxes_and_fees, grouping=True))

    ''' Totals Due '''
    due = sprint_premium_services
    if not family_member == "Hayden":
        due += plans_and_services + sprint_complete
    if family_member == "Ellie" or family_member == "Blair" or family_member == "Mama":
        due += equipment
    return locale.currency(due, grouping=True)


def bill(family_member):
    """ Billing Function """
    if family_member:
        print("Total Due: " + bill_ingredients(family_member))


family_members = ["Hayden", "Gavin", "Mama", "Ian", "Ellie", "Blair"]


def main(family):
    """ Family Members to Be Billed """
    print('\n', date.today().strftime("%A, %B %d, %Y"), '\n')
    for family_member in family:
        print(family_member)
        bill(family_member)
        print('\n')


main(family_members)
