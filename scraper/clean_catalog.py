from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_FILE = BASE_DIR / "data" / "catalog.json"
OUTPUT_FILE = BASE_DIR / "data" / "assessments.json"


def build_search_text(a):
    parts = []

    if a.get("name"):
        parts.append(f"Assessment Name: {a['name']}")

    if a.get("description"):
        parts.append(f"Description: {a['description']}")

    if a.get("keys"):
        parts.append("Categories: " + ", ".join(a["keys"]))

    if a.get("job_levels"):
        parts.append("Job Levels: " + ", ".join(a["job_levels"]))

    if a.get("languages"):
        parts.append("Languages: " + ", ".join(a["languages"]))

    if a.get("duration"):
        parts.append(f"Duration: {a['duration']}")

    if a.get("remote"):
        parts.append(f"Remote Testing: {a['remote']}")

    if a.get("adaptive"):
        parts.append(f"Adaptive Testing: {a['adaptive']}")

    return "\n".join(parts)


def clean_catalog():

    print("=" * 60)
    print("Loading catalog...")
    print("=" * 60)

    with open(RAW_FILE, encoding="utf-8") as f:
        catalog = json.load(f)

    assessments = []

    for item in catalog:

        assessment = {
            "id": item.get("entity_id", ""),
            "name": item.get("name", ""),
            "url": item.get("link", ""),
            "description": item.get("description", ""),
            "job_levels": item.get("job_levels", []),
            "languages": item.get("languages", []),
            "duration": item.get("duration", ""),
            "remote": item.get("remote", ""),
            "adaptive": item.get("adaptive", ""),
            "categories": item.get("keys", [])
        }

        assessment["search_text"] = build_search_text(item)

        assessments.append(assessment)

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            assessments,
            f,
            indent=2,
            ensure_ascii=False
        )

    print()
    print("=" * 60)
    print("Cleaning Complete")
    print("=" * 60)

    print(f"Saved {len(assessments)} assessments")
    print(f"Output : {OUTPUT_FILE}")


if __name__ == "__main__":
    clean_catalog()