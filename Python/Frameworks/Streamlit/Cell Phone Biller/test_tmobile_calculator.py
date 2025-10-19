# test_tmobile_calculator.py
import pytest
import tempfile
import json
from app import TMobileBillCalculator, ConfigurationError, ValidationError


class TestTMobileBillCalculator:

    def setup_method(self):
        """Setup before each test"""
        self.calc = TMobileBillCalculator()
        # Use a temporary config for testing
        self.test_config = self.calc.get_default_config()

    def test_default_configuration(self):
        """Test that default configuration loads correctly"""
        calc = TMobileBillCalculator()

        assert len(calc.family_members) == 7
        assert "Gavin" in calc.family_members
        assert calc.phone_numbers["Mama"] == "(502) 500-5480"
        assert calc.plan_groups["group_one"]["total_cost"] == 238.00

    def test_member_bill_calculation(self):
        """Test individual bill calculations"""
        bill = self.calc.calculate_member_bill("Gavin")

        assert "total" in bill
        assert "base_plan" in bill
        assert "discounts" in bill
        assert bill["total"] >= 0

    def test_discount_calculation(self):
        """Test discount calculations"""
        # Gavin should have AutoPay + Legacy Perk
        gavin_discounts = self.calc._calculate_discounts("Gavin")
        assert gavin_discounts == 10.00  # 5 + 5

        # Mama should have only AutoPay
        mama_discounts = self.calc._calculate_discounts("Mama")
        assert mama_discounts == 5.00

        # Hayden should have AutoPay + Line On Us
        hayden_discounts = self.calc._calculate_discounts("Hayden")
        assert hayden_discounts == 34.02  # 5 + 29.02

    def test_base_plan_cost(self):
        """Test base plan cost calculations"""
        # Group 1 members should have $47.60
        gavin_plan = self.calc._calculate_base_plan_cost("Gavin")
        assert gavin_plan == 47.60

        # Group 2 members should have $35.00
        hayden_plan = self.calc._calculate_base_plan_cost("Hayden")
        assert hayden_plan == 35.00

    def test_equipment_charges(self):
        """Test equipment charge calculations"""
        # Mama should have both iPhone and accessories
        mama_equipment = self.calc._calculate_equipment_charges("Mama")
        expected = 34.59 + 8.13  # iPhone + accessories
        assert mama_equipment == expected

        # Gavin should have no equipment
        gavin_equipment = self.calc._calculate_equipment_charges("Gavin")
        assert gavin_equipment == 0.0

    def test_protection_plans(self):
        """Test protection plan calculations"""
        # Protected members should have $18.00
        mama_protection = self.calc._calculate_protection_plans("Mama")
        assert mama_protection == 18.00

        # Hayden is not protected
        hayden_protection = self.calc._calculate_protection_plans("Hayden")
        assert hayden_protection == 0.0

    def test_plan_features(self):
        """Test plan feature calculations"""
        # Gavin should have Unlimited Plus
        gavin_features = self.calc._calculate_plan_features("Gavin")
        assert gavin_features == 10.00

        # Mama should not have Unlimited Plus
        mama_features = self.calc._calculate_plan_features("Mama")
        assert mama_features == 0.0

    def test_total_validation(self):
        """Test that totals validate correctly"""
        all_bills = {}
        for member in self.calc.family_members:
            all_bills[member] = self.calc.calculate_member_bill(member)

        # Should not raise an exception
        self.calc.validate_totals(all_bills)

    def test_invalid_member(self):
        """Test error handling for invalid family member"""
        with pytest.raises(ValueError):
            self.calc.calculate_member_bill("InvalidMember")

    def test_configuration_saving(self):
        """Test configuration saving and loading"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_config_file = f.name

        try:
            # Create calculator with temp config
            calc = TMobileBillCalculator()
            calc.config_file = temp_config_file

            # Save configuration
            calc.save_configuration()

            # Verify file was created
            import os
            assert os.path.exists(temp_config_file)

            # Verify content
            with open(temp_config_file, 'r') as f:
                saved_config = json.load(f)

            assert "family_members" in saved_config
            assert "plan_groups" in saved_config

        finally:
            # Clean up
            import os
            if os.path.exists(temp_config_file):
                os.unlink(temp_config_file)

    def test_negative_totals_prevention(self):
        """Test that negative totals are prevented"""
        # Create a scenario that could cause negative totals
        test_config = self.calc.get_default_config()
        test_config["one_time_charges"]["Hayden"] = -1000.00  # Large credit

        calc = TMobileBillCalculator()
        calc._apply_configuration(test_config)

        # Should handle without negative total
        hayden_bill = calc.calculate_member_bill("Hayden")
        assert hayden_bill["total"] >= 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
