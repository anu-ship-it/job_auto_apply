"""
Central config. No magic numbers scattered across files.
"""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

RESUME_PATH = BASE_DIR / "resume.pdf"          # your resume, drop it here
DB_PATH = BASE_DIR / "applications.db"          # tracks every application

# Greenhouse job board tokens are the "company" slug in their public API URL:
# https://boards-api.greenhouse.io/v1/boards/{token}/jobs
# Find a company's token by checking their careers page URL, e.g.
# boards.greenhouse.io/stripe -> token = "stripe"
GREENHOUSE_COMPANIES = [
    "stripe",
    "airbnb",
    "figma",
    # add more tokens here
]

# Lever uses: https://api.lever.co/v0/postings/{company}?mode=json
LEVER_COMPANIES = [
    "netflix",
    # add more
]

MIN_MATCH_SCORE = 0.15   # cosine similarity threshold, tune after first run
MAX_APPLICATIONS_PER_DAY = 25   # start low, raise once you trust the matcher
