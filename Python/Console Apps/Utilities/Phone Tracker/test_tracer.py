"""Regression tests for the command-line Phone Tracker."""
import unittest

from tracer import lookup_phone_number


class PhoneNumberLookupTests(unittest.TestCase):
    def test_requires_international_prefix(self):
        with self.assertRaises(ValueError) as context:
            lookup_phone_number("16502530000")
        self.assertIn("leading +", str(context.exception))

    def test_rejects_empty_input(self):
        with self.assertRaises(ValueError):
            lookup_phone_number("   ")

    def test_rejects_unparseable_or_invalid_number(self):
        with self.assertRaises(ValueError):
            lookup_phone_number("+1")
        with self.assertRaises(ValueError):
            lookup_phone_number("+12001230101")

    def test_returns_normalized_number_and_metadata(self):
        result = lookup_phone_number("+1 650 253 0000")
        self.assertEqual(result["number"], "+16502530000")
        self.assertTrue(result["region"])
        self.assertIn("carrier", result)
        self.assertIsInstance(result["time_zones"], tuple)

    def test_module_import_does_not_prompt_for_input(self):
        import tracer
        self.assertTrue(callable(tracer.main))


if __name__ == "__main__":
    unittest.main(verbosity=2)
