"""
discover_software.py
AI-Powered Software License Directory — Auto Discovery
Asks Gemini to suggest 100 new software tools not already in the CSV,
verifies their license info, and appends them to software_list.csv.
"""

import os
import sys
import json
import time
import requests
import pandas as pd
from datetime import date
from pathlib import Path
from google import genai

# ── Config ─────────────────────────────────────────────────────────────────────
GEMINI_KEY   = os.getenv("GEMINI_API_KEY", "")
CSV_PATH     = Path(__file__).parent.parent / "data" / "software_list.csv"
NEW_PER_RUN  = 100
GEMINI_MODEL = "gemini-3.6-flash"

VALID_CATEGORIES = [
    "Open Source",
    "Free for Home",
    "License Required",
    "License for Commercial",
    "Community Version",
]

# ── Gemini client ──────────────────────────────────────────────────────────────
client = genai.Client(api_key=GEMINI_KEY)

def call_gemini(prompt: str) -> str:
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
    )
    return response.text.strip().replace("```json", "").replace("```", "").strip()


# ── Load existing software names ───────────────────────────────────────────────
def load_existing_names(df: pd.DataFrame) -> list[str]:
    return [n.strip().lower() for n in df["Software Name"].dropna().tolist()]


# ── Step 1: Ask Gemini to suggest 20 new tools ────────────────────────────────
def discover_new_software(existing_names: list[str]) -> list[dict]:
    existing_str = "\n".join(f"- {n}" for n in existing_names)

    prompt = f"""
You are a software licensing expert building a directory of popular software tools.

The following software is ALREADY in our directory — do NOT suggest any of these:
{existing_str}

Your task: Suggest exactly {NEW_PER_RUN} well-known software tools NOT in the list above.
Pick from a variety of categories: developer tools, productivity apps, design tools,
databases, security tools, communication tools, creative software, cloud tools, etc.

For each tool, classify into EXACTLY ONE of these license categories:
1. "Open Source"            — Source available, free for all (MIT, GPL, Apache, etc.)
2. "Free for Home"          — Free for personal use only; commercial use requires payment
3. "License Required"       — Paid license required for any use
4. "License for Commercial" — Free personally, but paid license needed for business
5. "Community Version"      — Free community edition alongside paid enterprise tiers

Return ONLY a valid JSON array, no markdown, no explanation:
[
  {{
    "software_name": "Example App",
    "category": "Open Source",
    "license_status": "Free - Open Source",
    "official_url": "https://example.com",
    "notes": "One sentence describing the key licensing detail."
  }}
]
"""
    try:
        text = call_gemini(prompt)
        suggestions = json.loads(text)
        print(f"  Gemini suggested {len(suggestions)} new tools.")
        return suggestions
    except json.JSONDecodeError as e:
        print(f"[ERROR] JSON parse error from Gemini: {e}")
        return []
    except Exception as e:
        print(f"[ERROR] Gemini discovery failed: {e}")
        return []


# ── Step 2: Verify each suggestion ────────────────────────────────────────────
def verify_software(name: str, url: str) -> dict | None:
    prompt = f"""
Verify the current licensing status of "{name}" (official site: {url}).

Classify into EXACTLY ONE of:
1. "Open Source"
2. "Free for Home"
3. "License Required"
4. "License for Commercial"
5. "Community Version"

Return ONLY valid JSON, no markdown:
{{
  "software_name": "{name}",
  "category": "<one of the 5 above>",
  "license_status": "<concise status>",
  "official_url": "{url}",
  "notes": "<one sentence on the key licensing detail>",
  "confidence": "<high|medium|low>"
}}
"""
    try:
        text = call_gemini(prompt)
        return json.loads(text)
    except Exception as e:
        print(f"    [WARN] Verification failed for {name}: {e}")
        return None


# ── Step 3: Check URL reachability ────────────────────────────────────────────
def is_url_reachable(url: str, timeout: int = 8) -> bool:
    try:
        resp = requests.head(url, timeout=timeout, allow_redirects=True)
        return resp.status_code < 400
    except Exception:
        return False


# ── Main ───────────────────────────────────────────────────────────────────────
def run():
    print("=" * 60)
    print(f"AI Software Auto-Discovery  |  {GEMINI_MODEL}")
    print(f"CSV: {CSV_PATH}")
    print("=" * 60)

    if not CSV_PATH.exists():
        print(f"[ERROR] CSV not found at {CSV_PATH}")
        sys.exit(1)

    df = pd.read_csv(CSV_PATH)
    existing_names = load_existing_names(df)
    print(f"\n📋 Existing entries: {len(df)}")
    print(f"🔍 Asking Gemini to suggest {NEW_PER_RUN} new tools...\n")

    suggestions = discover_new_software(existing_names)
    if not suggestions:
        print("[EXIT] No suggestions returned. Exiting.")
        sys.exit(0)

    new_rows = []
    for s in suggestions:
        name = s.get("software_name", "").strip()
        if not name:
            continue
        if name.lower() in existing_names:
            print(f"  [SKIP] Already exists: {name}")
            continue

        print(f"\n  Verifying: {name}")
        url = s.get("official_url", "")

        if url and not is_url_reachable(url):
            print(f"    [WARN] URL unreachable: {url}")

        verified = verify_software(name, url)
        if not verified:
            verified = s

        category = verified.get("category", "Community Version")
        if category not in VALID_CATEGORIES:
            print(f"    [WARN] Invalid category '{category}' — defaulting to 'Community Version'")
            category = "Community Version"

        new_row = {
            "Software Name":  name,
            "Category":       category,
            "License Status": verified.get("license_status", ""),
            "Official URL":   verified.get("official_url", url),
            "Last Updated":   str(date.today()),
            "Notes":          verified.get("notes", ""),
        }

        confidence = verified.get("confidence", "?")
        print(f"    ✅ {category} | {new_row['License Status']} (confidence: {confidence})")
        new_rows.append(new_row)
        existing_names.append(name.lower())
        time.sleep(1.5)

    if not new_rows:
        print("\n[INFO] No new software to add this run.")
        sys.exit(0)

    new_df = pd.DataFrame(new_rows)
    updated_df = pd.concat([df, new_df], ignore_index=True)
    updated_df.to_csv(CSV_PATH, index=False)

    print(f"\n{'=' * 60}")
    print(f"✅ Added {len(new_rows)} new entries.")
    print(f"📊 Total entries now: {len(updated_df)}")
    print(f"💾 Saved to {CSV_PATH}")


if __name__ == "__main__":
    run()
