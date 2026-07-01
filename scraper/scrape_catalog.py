"""
Downloads the SHL Product Catalog and stores both the raw response
and a cleaned JSON version.
"""

from pathlib import Path
import json
import requests

CATALOG_URL = (
    "https://tcp-us-prod-rnd.shl.com/voiceRater/"
    "shl-ai-hiring/shl_product_catalog.json"
)

# Project Root
BASE_DIR = Path(__file__).resolve().parent.parent

# Root data folder
DATA_DIR = BASE_DIR / "data"

RAW_FILE = DATA_DIR / "raw_catalog.json"
CLEAN_FILE = DATA_DIR / "catalog.json"


def repair_json(text: str) -> str:
    """
    Repair malformed JSON by escaping invalid control characters
    inside string values.
    """

    repaired = []

    in_string = False
    escaped = False

    for ch in text:

        if escaped:
            repaired.append(ch)
            escaped = False
            continue

        if ch == "\\":
            repaired.append(ch)
            escaped = True
            continue

        if ch == '"':
            repaired.append(ch)
            in_string = not in_string
            continue

        if in_string:

            if ch == "\n":
                repaired.append("\\n")
                continue

            if ch == "\r":
                repaired.append("\\r")
                continue

            if ch == "\t":
                repaired.append("\\t")
                continue

        repaired.append(ch)

    return "".join(repaired)


def download_catalog():

    print("=" * 60)
    print("Downloading SHL Product Catalog")
    print("=" * 60)

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    response = requests.get(
        CATALOG_URL,
        timeout=60,
    )

    response.raise_for_status()

    print("Status Code :", response.status_code)

    RAW_FILE.write_text(
        response.text,
        encoding="utf-8"
    )

    print("Raw catalog saved to:")
    print(RAW_FILE)

    raw_text = response.text

    try:

        catalog = json.loads(raw_text)

        print("JSON parsed successfully.")

    except json.JSONDecodeError as e:

        print("\nMalformed JSON detected.")
        print(e)

        print("\nRepairing...")

        repaired = repair_json(raw_text)

        catalog = json.loads(repaired)

        print("Repair Successful.")

    CLEAN_FILE.write_text(

        json.dumps(
            catalog,
            indent=2,
            ensure_ascii=False
        ),

        encoding="utf-8"

    )

    print("\nClean catalog saved to:")
    print(CLEAN_FILE)

    if isinstance(catalog, list):
        print(f"\nTotal Assessments : {len(catalog)}")

    print("\nDone.")


if __name__ == "__main__":
    download_catalog()