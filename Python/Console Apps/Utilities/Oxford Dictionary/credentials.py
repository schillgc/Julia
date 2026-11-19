"""Load Oxford Dictionaries API credentials from the local environment."""

import os

app_id = os.environ.get("OXFORD_DICTIONARIES_APP_ID", "")
app_key = os.environ.get("OXFORD_DICTIONARIES_APP_KEY", "")

if not app_id.strip() or not app_key.strip():
    raise RuntimeError(
        "Set OXFORD_DICTIONARIES_APP_ID and OXFORD_DICTIONARIES_APP_KEY "
        "in your local environment before running this example."
    )
