import locale
from datetime import date

locale.setlocale(locale.LC_ALL, 'English_United States.1252')


def bill_ingredients(family_member):
    """ Cell Phone Plan Rates Subtotal """
    number_of_lines = len(family_members)
    lines_one_and_two = 123
    kid_lines = 2
    additional_lines = number_of_lines - kid_lines - 2  # Lines 1 & 2 + Hayden & Wilder's Free Lines Excluded
    unlimited_basic_phone_plan: float = (
            lines_one_and_two + (additional_lines * 30))

    equally_divided_base_phone_plan_charge = unlimited_basic_phone_plan / (number_of_lines - kid_lines) \
        # Hayden and Wilder exempt
    if not family_member == "Hayden" and not family_member == "Wilder":
        print("Equally Divided Plan:", locale.currency(equally_divided_base_phone_plan_charge, grouping=True))

    ''' Equipment '''
    equipment = 0
    samsung_lease = True
    apple_lease = True
    if date.today() < date(2024, 10, 31) and samsung_lease:
        if family_member == "Gavin":
            equipment += 50
    if date.today() < date(2024, 4, 30) and apple_lease:
        if family_member == "Ian":
            equipment += 33.34
    if date.today() < date(2024, 7, 31) and apple_lease:
        if family_member == "Mama":
            equipment += 33.34
    if date.today() < date(2026, 5, 31) and apple_lease:
        if family_member == "Blair":
            equipment += 41.67
    if not equipment == 0:
        print("Equipment:", locale.currency(equipment, grouping=True))

    ''' Auto-Payment & Other Discounts '''
    discounts = 0
    auto_pay = False

    if not family_member == "Hayden" and not family_member == "Wilder":
        auto_pay_plan_discount = 5
        if auto_pay:
            discounts += auto_pay_plan_discount
        else:
            print("You can save by auto-paying")

    if family_member == "Gavin" and date.today() < date(2025, 1, 31):
        sprint_perks_discount = 5
        samsung_trade = 33.34
        discounts += sprint_perks_discount + samsung_trade
    if family_member == "Hayden" and family_member == "Wilder":
        line_on_us = 24.21
        rate_plan_credit = 0.79
        discounts += line_on_us + rate_plan_credit
    if family_member == "Mama" and date.today() < date(2024, 7, 31):
        apple_trade_in = 16.67
        discounts += apple_trade_in
    if family_member == "Ian" and date.today() < date(2024, 4, 30):
        apple_trade_in = 25
        discounts += apple_trade_in
    if family_member == "Blair" and date.today() < date(2025, 6, 30):
        apple_trade_in = 0
        discounts += apple_trade_in

    if not discounts == 0:
        print("Discounts:", locale.currency(discounts, grouping=True))

    ''' Plan & Equipment Subtotal '''
    net_plan_and_equipment = (equally_divided_base_phone_plan_charge + equipment) - discounts
    if not family_member == "Hayden" and not family_member == "Wilder":
        print("Plan & Equipment (After Discounts):", locale.currency(net_plan_and_equipment, grouping=True))

    ''' T-Mobile Protection 360 & Premium Services Subtotal '''
    protection_360_tier_3 = 13
    protection_360_tier_5 = 18
    services = 0
    protection_plan_for_hayden = True
    if protection_plan_for_hayden:
        if not family_member == "Hayden" and not family_member == "Wilder":
            # Hayden's Protection Plan
            services += (protection_360_tier_3 / (number_of_lines - kid_lines))
    if not family_member == "Hayden" and not family_member == "Wilder":
        unlimited_plus = 10
        services += (unlimited_plus / (number_of_lines - kid_lines)) + protection_360_tier_5
    if not services == 0:
        print("Services:", locale.currency(
            services, grouping=True))

    ''' Usage '''
    usage = 0
    if not usage == 0:
        print("Usage: ", locale.currency(usage, grouping=True))

    ''' Surcharges Subtotal '''
    surcharges = 0
    if not surcharges == 0:
        print("Surcharges:", locale.currency(surcharges, grouping=True))

    ''' Government Taxes & Fees Subtotal '''
    government_taxes_and_fees = 0
    sales_tax = 0

    if not family_member == "Hayden" and not family_member == "Wilder":
        sales_tax += 6.18
        government_taxes_and_fees += (sales_tax / (number_of_lines - kid_lines))

    if not government_taxes_and_fees == 0:
        print("Government Taxes & Fees:", locale.currency(
            government_taxes_and_fees, grouping=True))

    ''' Totals Due '''
    due = 0
    if not family_member == "Hayden" and not family_member == "Wilder":
        due += net_plan_and_equipment + services + usage + surcharges + government_taxes_and_fees
    if family_member == "Hayden" and family_member == "Wilder":
        due += usage
    return locale.currency(due, grouping=True)


def bill(family_member):
    """ Billing Function """
    if family_member:
        print("Total Due: " + bill_ingredients(family_member))



family_members = ["Gavin", "Mama", "Ian", "Ellie", "Blair", "Hayden", "Wilder"]


def main(family):
    """ Family Members to Be Billed """
    print('\n', date.today().strftime("%A, %B %d, %Y"), '\n')
    for family_member in family:
        print(family_member)
        bill(family_member)
        print('\n')

main(family_members)
