"""Local-only configuration for Code Describer."""

import os

api_key = os.environ.get("OPENAI_API_KEY", "")
if not api_key.strip():
    raise RuntimeError(
        "Set OPENAI_API_KEY in the environment before running Code Describer."
    )
