"""
Orchestrator. Run this daily (cron/Task Scheduler) once you trust it.

Flow:
1. Parse resume -> text
2. Pull jobs from Greenhouse + Lever company lists
3. Score jobs against resume
4. Filter to top matches above threshold, capped at MAX_APPLICATIONS_PER_DAY
5. Skip anything already applied to
6. Print matches for review (v1: human-in-the-loop, no blind auto-submit)
"""
import config
from resume_parser import extract_text
from job_sources import greenhouse, lever
from matcher import score_jobs, filter_matches
from tracker import init_db, already_applied, log_application


def run():
    if not config.RESUME_PATH.exists():
        print(f"Put your resume at {config.RESUME_PATH} first.")
        return

    init_db(config.DB_PATH)

    print("Parsing resume...")
    resume_text = extract_text(config.RESUME_PATH)

    print("Fetching jobs...")
    jobs = []
    jobs += greenhouse.fetch_all(config.GREENHOUSE_COMPANIES)
    jobs += lever.fetch_all(config.LEVER_COMPANIES)
    print(f"  {len(jobs)} jobs fetched")

    # drop jobs we've already applied to before we even score them
    jobs = [j for j in jobs if not already_applied(config.DB_PATH, j["job_id"], j["source"])]
    print(f"  {len(jobs)} new jobs (not previously applied)")

    print("Scoring against resume...")
    scored = score_jobs(resume_text, jobs)
    matches = filter_matches(scored, config.MIN_MATCH_SCORE, config.MAX_APPLICATIONS_PER_DAY)

    print(f"\nTop {len(matches)} matches:\n")
    for j in matches:
        print(f"  [{j['score']:.3f}] {j['title']} @ {j['company']} ({j['source']}) -> {j['url']}")

    # v1: log as 'skipped' for review, NOT auto-applied. Wire in form_filler
    # here once you've manually verified the selectors work on a few of these.
    for j in matches:
        log_application(config.DB_PATH, j, status="skipped")

    print("\nLogged as 'skipped' pending review. Nothing was auto-submitted.")
    print("Once you've verified form_filler.py against real Greenhouse forms,")
    print("wire it into this loop and flip status to 'applied'.")


if __name__ == "__main__":
    run()
