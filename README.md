# job_auto_apply

Python automation that matches your resume against Greenhouse/Lever job
postings and (eventually, once you trust it) auto-fills applications.

## Why Greenhouse/Lever and not LinkedIn/Indeed?
Both expose public JSON APIs — no HTML scraping, no anti-bot fights, no ToS
violation. LinkedIn/Indeed scraping is fragile and against their ToS; adding
it is a stretch goal, not v1.

## Setup
```bash
pip install -r requirements.txt
playwright install chromium
```

Drop your resume at `job_auto_apply/resume.pdf` (or edit `config.py` to
point elsewhere / use `.docx`).

Edit `config.py`:
- `GREENHOUSE_COMPANIES` / `LEVER_COMPANIES` — company tokens (find from
  their careers page URL, e.g. `boards.greenhouse.io/stripe` → `stripe`)
- `MIN_MATCH_SCORE` — similarity threshold, tune after seeing real scores
- `MAX_APPLICATIONS_PER_DAY` — start low (25), raise once matching is
  trustworthy

## Run
```bash
python main.py
```

Right now this **only matches and logs — it does not submit anything.**
That's intentional. Get the matching quality right first; auto-submitting
bad matches wastes your applications and can burn recruiter goodwill just
as easily as an actual human sending bad applications does.

## Current state / what's actually done vs stubbed
- ✅ Resume parsing (PDF/DOCX)
- ✅ Job fetching from Greenhouse + Lever public APIs
- ✅ TF-IDF matching + scoring
- ✅ SQLite tracking (no duplicate applications)
- ⚠️ Form filler: working Playwright skeleton, but selectors are unverified
  against a live form. You need to run it against a real Greenhouse job page,
  open devtools, and confirm/fix the field selectors before trusting it.
- ❌ Auto-submit: deliberately disabled until you've verified the filler.
- ❌ LinkedIn/Indeed: not built. Legal/ToS risk (account ban) makes this a
  deliberate later decision, not a default.

## Next steps, in order
1. Add your real company target list to `config.py`, run `main.py`, sanity
   check whether the top matches actually make sense for your resume.
2. Tune `MIN_MATCH_SCORE` based on step 1.
3. Pick ONE company from your matches, manually open their Greenhouse
   application form, inspect field IDs, fix `form_filler.py` selectors.
4. Test `apply_to_greenhouse_job` with `headless=False` so you can watch it
   fill the form — do NOT uncomment the submit line until you've watched it
   fill correctly multiple times.
5. Only then wire `form_filler` into `main.py` and flip auto-submit on.
