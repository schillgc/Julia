"""Look up an English word using the Oxford Dictionaries API."""

import json
import os
from urllib.parse import quote

import requests


LANGUAGE = "en"
DEFAULT_WORD = "euphoria"


def main():
    app_id = os.environ.get("OXFORD_DICTIONARIES_APP_ID", "").strip()
    app_key = os.environ.get("OXFORD_DICTIONARIES_APP_KEY", "").strip()
    if not app_id or not app_key:
        raise SystemExit(
            "Set OXFORD_DICTIONARIES_APP_ID and OXFORD_DICTIONARIES_APP_KEY "
            "before running this example."
        )

    word_id = os.environ.get("OXFORD_DICTIONARIES_WORD", DEFAULT_WORD).strip()
    if not word_id:
        raise SystemExit("Set OXFORD_DICTIONARIES_WORD to a non-empty word.")

    url = (
        "https://od-api.oxforddictionaries.com/api/v2/entries/"
        f"{LANGUAGE}/{quote(word_id.lower(), safe='')}"
    )
    try:
        response = requests.get(
            url,
            headers={"app_id": app_id, "app_key": app_key},
            timeout=(5, 20),
        )
        response.raise_for_status()
        result = response.json()
    except requests.HTTPError as error:
        status = error.response.status_code if error.response is not None else "unknown"
        raise SystemExit(f"Oxford Dictionaries API returned HTTP {status}.") from None
    except requests.RequestException:
        raise SystemExit("Oxford Dictionaries API request failed.") from None
    except ValueError:
        raise SystemExit("Oxford Dictionaries API returned invalid JSON.") from None

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
