import locale
from datetime import date
from typing import Dict, List

# Set locale for currency formatting
locale.setlocale(locale.LC_ALL, 'English_United States.1252')


class CellPhoneBillCalculator:
    """Calculator for family cell phone bill distribution"""

    def __init__(self):
        self.family_members = ["Mama", "Ellie", "Blair", "Gavin", "Hayden", "Ian", "Wilder"]
        self.today = date.today()

        # Plan configuration
        self.plan_rates = {
            "line_one": 73.00,
            "line_two": 50.00,
            "third_generation_lines": 30.00,
            "additional_line_rate": 30.00
        }

        # Discount configuration
        self.discounts_config = {
            "auto_pay": 5.00,
            "sprint_perks": 5.00,
            "line_on_us": 25.00
        }

        # Equipment configuration
        self.equipment_config = {
            "samsung_a11_lease_end": date(2022, 12, 25),
            "samsung_a11_monthly": 7.50
        }

        # Protection plans configuration
        self.protection_plans = {
            "hayden_protection": 0.00,
            "premium_plans": {
                "Blair": 19.00,
                "Gavin": 19.00,
                "Ellie": 15.00,
                "Ian": 15.00
            }
        }

    def calculate_base_plan_cost(self) -> Dict[str, float]:
        """Calculate the base unlimited plan cost distribution"""
        num_lines = len(self.family_members)

        # Calculate total base plan cost
        additional_lines_cost = self.plan_rates["additional_line_rate"] * (num_lines - 3)
        total_base_cost = (
                self.plan_rates["line_one"] +
                self.plan_rates["line_two"] +
                self.plan_rates["third_generation_lines"] +
                additional_lines_cost
        )

        # Calculate equal distribution (before Hayden's special rate)
        equal_share = total_base_cost / num_lines

        # Adjust for Hayden's special rate
        base_costs = {}
        hayden_adjustment = (equal_share - self.plan_rates["third_generation_lines"]) / (num_lines - 1)

        for member in self.family_members:
            if member == "Hayden" or member == "Wilder":
                base_costs[member] = self.plan_rates["third_generation_lines"]
            else:
                base_costs[member] = equal_share + hayden_adjustment

        return base_costs

    def calculate_discounts(self, family_member: str) -> float:
        """Calculate applicable discounts for a family member"""
        total_discount = 0.0

        # Auto-pay discount for everyone
        total_discount += self.discounts_config["auto_pay"]

        # Member-specific discounts
        if family_member == "Gavin":
            total_discount += self.discounts_config["sprint_perks"]
        elif family_member == "Hayden" or family_member == "Wilder":
            total_discount += self.discounts_config["line_on_us"]

        return total_discount

    def calculate_equipment_charges(self, family_member: str) -> float:
        """Calculate equipment charges for a family member"""
        equipment_charge = 0.0

        # Samsung A11 lease charges (shared by Mama, Ellie, Blair)
        if (self.today < self.equipment_config["samsung_a11_lease_end"] and
                family_member in ["Mama", "Ellie", "Blair"]):
            equipment_charge = self.equipment_config["samsung_a11_monthly"] / 3

        return equipment_charge

    def calculate_protection_plans(self, family_member: str) -> float:
        """Calculate protection plan charges for a family member"""
        protection_charge = 0.0

        # Hayden's protection plan (shared by others except Ian)
        if family_member not in ["Hayden", "Ian"]:
            protection_charge += (self.protection_plans["hayden_protection"] /
                                  (len(self.family_members) - 2))

        # Individual premium protection plans
        protection_charge += self.protection_plans["premium_plans"].get(family_member, 0.0)

        return protection_charge

    def calculate_member_bill(self, family_member: str) -> Dict[str, float]:
        """Calculate complete bill for a family member"""
        if family_member not in self.family_members:
            raise ValueError(f"Unknown family member: {family_member}")

        base_costs = self.calculate_base_plan_cost()
        base_charge = base_costs[family_member]
        discounts = self.calculate_discounts(family_member)
        equipment_charges = self.calculate_equipment_charges(family_member)
        protection_charges = self.calculate_protection_plans(family_member)

        # Calculate final charges
        plans_and_services = base_charge - discounts
        total_charges = plans_and_services + equipment_charges + protection_charges

        return {
            "base_plan": base_charge,
            "discounts": discounts,
            "plans_and_services": plans_and_services,
            "equipment": equipment_charges,
            "protection": protection_charges,
            "total": total_charges
        }

    def print_member_bill(self, family_member: str):
        """Print formatted bill for a family member"""
        bill = self.calculate_member_bill(family_member)

        print(f"\n=== {family_member}'s Cell Phone Bill ===")
        print(f"Base Plan: {locale.currency(bill['base_plan'], grouping=True)}")

        if bill['discounts'] > 0:
            print(f"Discounts: -{locale.currency(bill['discounts'], grouping=True)}")

        print(f"Plans & Services: {locale.currency(bill['plans_and_services'], grouping=True)}")

        if bill['equipment'] > 0:
            print(f"Equipment: {locale.currency(bill['equipment'], grouping=True)}")

        if bill['protection'] > 0:
            print(f"Protection Plans: {locale.currency(bill['protection'], grouping=True)}")

        print(f"TOTAL: {locale.currency(bill['total'], grouping=True)}")

    def print_all_bills(self):
        """Print bills for all family members"""
        print("FAMILY CELL PHONE BILL BREAKDOWN")
        print("=" * 40)

        total_family_bill = 0.0
        for member in self.family_members:
            bill = self.calculate_member_bill(member)
            total_family_bill += bill['total']
            self.print_member_bill(member)

        print(f"\nTOTAL FAMILY BILL: {locale.currency(total_family_bill, grouping=True)}")


# Example usage
def main():
    calculator = CellPhoneBillCalculator()

    # Print bill for a specific member
    calculator.print_member_bill("Hayden")

    # Print all bills
    calculator.print_all_bills()


if __name__ == "__main__":
    main()