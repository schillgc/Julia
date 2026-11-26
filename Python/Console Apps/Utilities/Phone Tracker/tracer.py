"""Look up public numbering metadata for an explicitly international phone number.

This tool uses numbering metadata bundled with phonenumbers. It does not locate
a device, identify a subscriber, or access call records.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any

import phonenumbers
import pytz
from phonenumbers import carrier, geocoder, timezone


def lookup_phone_number(raw_number: str) -> dict[str, Any]:
    """Validate an international number and return public numbering metadata."""
    if not isinstance(raw_number, str) or not raw_number.strip():
        raise ValueError("Enter a phone number with a leading + and country code.")

    candidate = raw_number.strip()
    if not candidate.startswith("+"):
        raise ValueError("Include the leading + and international country code.")

    try:
        number = phonenumbers.parse(candidate, None)
    except phonenumbers.NumberParseException as exc:
        raise ValueError(f"Unable to parse phone number: {exc}") from exc

    if not phonenumbers.is_possible_number(number):
        raise ValueError("The number is not a possible international phone number.")
    if not phonenumbers.is_valid_number(number):
        raise ValueError("The number is not a valid phone number for its numbering plan.")

    zones = tuple(timezone.time_zones_for_number(number))
    details: dict[str, Any] = {
        "number": phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.E164),
        "region": geocoder.description_for_number(number, "en") or "Unknown",
        "carrier": carrier.name_for_number(number, "en") or "Unknown",
        "time_zones": zones,
    }

    for zone_name in zones:
        try:
            zone = pytz.timezone(zone_name)
        except pytz.UnknownTimeZoneError:
            continue
        details["local_time"] = datetime.now(zone).strftime("%B %d, %Y %I:%M %p")
        break

    return details


def main() -> int:
    """Run the interactive command-line lookup."""
    try:
        raw_number = input("Enter an international phone number (for example, +16502530000): ")
        details = lookup_phone_number(raw_number)
    except (ValueError, EOFError, KeyboardInterrupt) as exc:
        print(f"Phone number lookup unavailable: {exc}")
        return 2

    print(f"Number: {details['number']}")
    print(f"Region: {details['region']}")
    print(f"Carrier: {details['carrier']}")
    if details["time_zones"]:
        print("Time zone(s): " + ", ".join(details["time_zones"]))
    if details.get("local_time"):
        print(f"Local time: {details['local_time']}")
    else:
        print("Local time: unavailable for this number")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
