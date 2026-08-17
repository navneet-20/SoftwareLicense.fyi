"""
discover_software.py
AI-Powered Software License Directory — Auto Discovery
Asks Gemini to suggest 10 new software tools not already in the CSV,
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
NEW_PER_RUN  = 10
GEMINI_MODEL = "gemini-2.0-flash"

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
