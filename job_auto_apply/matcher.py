"""
Scores each job posting against your resume using TF-IDF + cosine similarity.

Why not embeddings/an LLM call for this? Because TF-IDF is:
- free (no API cost, no rate limits when scoring hundreds of jobs/day)
- deterministic and debuggable (you can inspect *why* a score was high)
- good enough for this problem: resume-to-JD matching is fundamentally a
  keyword/skill overlap problem, not a deep-semantic one.

Swap this for embeddings later ONLY if you find TF-IDF's matches are bad in
practice. Don't pre-optimize before you have evidence it's needed.
"""
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def _strip_html(text: str) -> str:
    return re.sub(r"<[^>]+>", " ", text or "")


def score_jobs(resume_text: str, jobs: list[dict]) -> list[dict]:
    """Adds a 'score' key to each job dict, sorted descending."""
    corpus = [resume_text] + [_strip_html(j["description"]) for j in jobs]

    vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
    tfidf_matrix = vectorizer.fit_transform(corpus)

    resume_vec = tfidf_matrix[0:1]
    job_vecs = tfidf_matrix[1:]

    scores = cosine_similarity(resume_vec, job_vecs)[0]

    for job, score in zip(jobs, scores):
        job["score"] = round(float(score), 4)

    return sorted(jobs, key=lambda j: j["score"], reverse=True)


def filter_matches(scored_jobs: list[dict], min_score: float, max_count: int) -> list[dict]:
    matches = [j for j in scored_jobs if j["score"] >= min_score]
    return matches[:max_count]
