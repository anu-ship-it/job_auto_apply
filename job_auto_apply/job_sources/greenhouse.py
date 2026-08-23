"""
Greenhouse exposes a public, undocumented-but-stable JSON API per company.
This is NOT scraping - it's a plain GET request to a JSON endpoint, so it's
faster, more reliable, and doesn't trip anti-bot defenses.

Endpoint: https://boards-api.greenhouse.io/v1/boards/{token}/jobs?content=true
"""
import requests

BASE_URL = "https://boards-api.greenhouse.io/v1/boards/{token}/jobs"


def fetch_jobs(company_token: str) -> list[dict]:
    """Returns a list of {title, location, url, description, company} dicts."""
    resp = requests.get(
        BASE_URL.format(token=company_token),
        params={"content": "true"},
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()

    jobs = []
    for job in data.get("jobs", []):
        jobs.append({
            "source": "greenhouse",
            "company": company_token,
            "title": job.get("title", ""),
            "location": (job.get("location") or {}).get("name", ""),
            "url": job.get("absolute_url", ""),
            "description": job.get("content", ""),  # HTML, strip tags in matcher
            "job_id": str(job.get("id", "")),
        })
    return jobs


def fetch_all(company_tokens: list[str]) -> list[dict]:
    all_jobs = []
    for token in company_tokens:
        try:
            all_jobs.extend(fetch_jobs(token))
        except requests.RequestException as e:
            print(f"[greenhouse] failed to fetch {token}: {e}")
    return all_jobs
