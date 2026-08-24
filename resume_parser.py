"""
Turns a resume file (PDF or DOCX) into plain text we can feed to the matcher.

No LLM call here on purpose - text extraction doesn't need one, and calling
an API for something a library does deterministically is exactly the kind
of over-engineering we're avoiding.
"""
from pathlib import Path


def extract_text(resume_path: Path) -> str:
    suffix = resume_path.suffix.lower()

    if suffix == ".pdf":
        import pdfplumber
        text_chunks = []
        with pdfplumber.open(resume_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_chunks.append(page_text)
        return "\n".join(text_chunks)

    if suffix == ".docx":
        import docx
        doc = docx.Document(resume_path)
        return "\n".join(p.text for p in doc.paragraphs)

    raise ValueError(f"Unsupported resume format: {suffix}. Use .pdf or .docx")


if __name__ == "__main__":
    from config import RESUME_PATH
    if not RESUME_PATH.exists():
        print(f"No resume found at {RESUME_PATH}. Drop your resume there first.")
    else:
        print(extract_text(RESUME_PATH)[:500])
