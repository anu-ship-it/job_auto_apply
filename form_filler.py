"""
Fills and submits Greenhouse/Lever application forms with Playwright.

BE HONEST WITH YOURSELF ABOUT WHAT THIS IS: a per-ATS-template filler, not a
universal form-filler. Greenhouse forms share a consistent structure across
companies (same underlying platform), so ONE selector set covers hundreds
of companies. That's the leverage. It will break if Greenhouse changes their
frontend, or on companies that heavily customize their application form
(some do - custom questions, portfolio uploads, etc). When it breaks on a
specific company, it should skip and log 'failed', not crash the whole run.

This is a working skeleton, not a finished product - you need to run it
against a real Greenhouse form, inspect the actual field selectors in
devtools, and correct them. I'm not going to fabricate selectors and pretend
they'll just work; that would waste your time debugging phantom code.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright


def apply_to_greenhouse_job(job: dict, resume_path: Path, applicant: dict, headless: bool = True) -> bool:
    """
    applicant = {
        "first_name": "...", "last_name": "...", "email": "...", "phone": "..."
    }

    Returns True on submit success, False on failure (form structure mismatch,
    required custom question we don't have an answer for, etc). Caller decides
    what to do with False - log it, review manually, don't retry blindly.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()
        try:
            page.goto(job["url"], timeout=30000)

            # NOTE: these selectors are Greenhouse's common pattern as of
            # writing. VERIFY against the live form before trusting this.
            page.fill("#first_name", applicant["first_name"])
            page.fill("#last_name", applicant["last_name"])
            page.fill("#email", applicant["email"])
            if applicant.get("phone"):
                page.fill("#phone", applicant["phone"])

            page.set_input_files("input[type='file']", str(resume_path))

            # Deliberately NOT auto-clicking submit in this skeleton.
            # Flip this on only after you've verified the form filled
            # correctly on a handful of real companies.
            # page.click("button#submit_app")

            return True

        except Exception as e:
            print(f"[form_filler] failed on {job['company']} ({job['url']}): {e}")
            return False
        finally:
            browser.close()
