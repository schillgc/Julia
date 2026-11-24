# T-Mobile Bill Calculator

A Streamlit tool for entering a mobile-plan bill locally, allocating charges to configurable lines, reviewing the split, and exporting a spreadsheet or CSV.

## Privacy first

This repository contains only the application code and a synthetic example configuration. **Do not commit a real `tmobile_config.json`, generated workbook, CSV export, phone number, member name, account identifier, statement, or payment information.** The local configuration is excluded by the root `.gitignore`; keep the repository's real billing data on a private device or in an approved private storage location.

Create a private configuration from the example:

```bash
cp tmobile_config.example.json tmobile_config.json
```

Edit `tmobile_config.json` locally. The application also supports a custom path through `TMOBILE_CONFIG_FILE` so the file can live outside the repository.

## Features

- Dashboard with bill totals and per-line allocation
- Individual line breakdowns and detailed analysis
- Configurable plan groups, discounts, equipment, protection and one-time adjustments
- Optional reconciliation against an expected invoice total
- CSV and Excel exports; Excel files are generated in memory rather than written beside the source

## Install and run

Python 3.10 or newer is recommended.

```bash
python -m venv .venv
# Activate the environment, then:
python -m pip install -r requirements.txt
streamlit run app.py
```

## Configuration model

The example file uses fictional lines and sample values. Replace these locally with the details from the invoice you are authorized to process.

- `family_members` and `phone_numbers`: local line labels and optional phone labels
- `plan_groups`: group membership and group plan totals
- `discounts_config`: discount values and the line labels to which each discount applies
- `equipment_config`: installment amounts and assigned line labels
- `protection_plans`: protection-plan amount and covered line labels
- `plan_features`: optional feature price and assigned line
- `one_time_charges`: line-specific credits or adjustments
- `expected_total_bill`: optional invoice total used for reconciliation; leave `null` to disable this check until a current invoice amount is entered

The application derives the per-line plan amount from each configured group's total and member count. It does not contain a personal expected bill total or default family/member identifiers.

## Exports

CSV data is returned as a download from the current Streamlit session. Excel exports are assembled in memory. Never commit exported files; the repository ignores common bill-workbook and configuration filenames as a second line of defense.
