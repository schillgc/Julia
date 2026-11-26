"""Regression tests using only the calculator's synthetic starter configuration."""
import csv
import io
import tempfile
import unittest
from pathlib import Path

from app import (
    TMobileBillCalculator,
    ValidationError,
    format_currency,
)


class TMobileBillCalculatorTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.config_path = Path(self.temp_dir.name) / "synthetic-config.json"
        self.calculator = TMobileBillCalculator(config_file=str(self.config_path))

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_default_configuration_is_synthetic(self):
        self.assertEqual(self.calculator.family_members, ["Line A", "Line B"])
        self.assertEqual(
            self.calculator.phone_numbers,
            {"Line A": "Not configured", "Line B": "Not configured"},
        )
        self.assertIsNone(self.calculator.expected_total_bill)

    def test_member_bill_uses_group_plan_allocation(self):
        bill = self.calculator.calculate_member_bill("Line A")
        self.assertEqual(bill["base_plan"], 50.0)
        self.assertEqual(bill["discounts"], 0.0)
        self.assertEqual(bill["total"], 50.0)

    def test_all_bills_reconcile_when_expected_total_is_configured(self):
        self.calculator.expected_total_bill = 90.0
        bills = self.calculator.calculate_all_bills()
        self.assertEqual(set(bills), {"Line A", "Line B"})
        self.assertAlmostEqual(sum(row["total"] for row in bills.values()), 90.0)

    def test_total_reconciliation_rejects_a_mismatch(self):
        self.calculator.expected_total_bill = 89.0
        with self.assertRaises(ValidationError):
            self.calculator.calculate_all_bills()

    def test_unknown_line_is_rejected(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_member_bill("Unknown Line")

    def test_configuration_round_trips_to_private_temp_file(self):
        self.assertTrue(self.config_path.is_file())
        self.calculator.save_configuration()
        restored = TMobileBillCalculator(config_file=str(self.config_path))
        self.assertEqual(restored.family_members, ["Line A", "Line B"])
        self.assertEqual(restored.plan_groups["group_one"]["total_cost"], 50.0)

    def test_csv_export_contains_only_configured_synthetic_lines(self):
        bills = self.calculator.calculate_all_bills()
        content = self.calculator.export_to_csv(bills)
        rows = list(csv.DictReader(io.StringIO(content)))
        self.assertEqual([row["Member"] for row in rows], ["Line A", "Line B"])
        self.assertEqual(rows[0]["Phone Number"], "Not configured")

    def test_excel_export_is_returned_in_memory(self):
        bills = self.calculator.calculate_all_bills()
        content = self.calculator.export_to_excel(bills)
        self.assertIsInstance(content, bytes)
        self.assertTrue(content.startswith(b"PK"))
        self.assertGreater(len(content), 100)

    def test_currency_formatting_is_locale_independent(self):
        self.assertEqual(format_currency(1234.5), "$1,234.50")
        self.assertEqual(format_currency(-9.1), "$-9.10")


if __name__ == "__main__":
    unittest.main(verbosity=2)
