"""
Lever also exposes a public JSON API per company posting board.
Endpoint: https://api.lever.co/v0/postings/{company}?mode=json
"""
import requests

BASE_URL = "https://api.lever.co/v0/postings/{company}"


def fetch_jobs(company: str) -> list[dict]:
    resp = requests.get(
        BASE_URL.format(company=company),
        params={"mode": "json"},
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()

    jobs = []
    for job in data:
        jobs.append({
            "source": "lever",
            "company": company,
            "title": job.get("text", ""),
            "location": (job.get("categories") or {}).get("location", ""),
            "url": job.get("hostedUrl", ""),
            "description": job.get("descriptionPlain", ""),
            "job_id": job.get("id", ""),
        })
    return jobs


def fetch_all(companies: list[str]) -> list[dict]:
    all_jobs = []
    for company in companies:
        try:
            all_jobs.extend(fetch_jobs(company))
        except requests.RequestException as e:
            print(f"[lever] failed to fetch {company}: {e}")
    return all_jobs
