import re
from typing import Union


def compute_ats_score(cv_text: str) -> float:
    score = 0.0

    sections = ["experience", "education", "skills", "summary", "objective", "projects", "certifications"]
    found_sections = sum(1 for s in sections if s in cv_text.lower())
    score += min(found_sections / len(sections), 1.0) * 30

    bullet_count = len(re.findall(r"^\s*[•\-\*\u2022]", cv_text, re.MULTILINE))
    score += min(bullet_count / 10, 1.0) * 20

    email_present = bool(re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", cv_text))
    phone_present = bool(re.search(r"(\+?\d[\d\s\-().]{7,}\d)", cv_text))
    score += 10 if email_present else 0
    score += 10 if phone_present else 0

    word_count = len(cv_text.split())
    if 300 <= word_count <= 1000:
        score += 20
    elif 150 <= word_count < 300 or 1000 < word_count <= 1500:
        score += 10

    date_patterns = re.findall(r"\b(19|20)\d{2}\b", cv_text)
    score += min(len(date_patterns) / 4, 1.0) * 10

    return round(min(score, 100), 1)


def compute_keyword_score(keywords: dict) -> float:
    found = len(keywords.get("found", []))
    partial = len(keywords.get("partial", []))
    missing = len(keywords.get("missing", []))
    total = found + partial + missing
    if total == 0:
        return 50.0
    score = ((found * 1.0 + partial * 0.5) / total) * 100
    return round(min(score, 100), 1)


def compute_format_score(cv_text: str) -> float:
    score = 0.0

    lines = [l for l in cv_text.splitlines() if l.strip()]
    if lines:
        avg_len = sum(len(l) for l in lines) / len(lines)
        if 40 <= avg_len <= 120:
            score += 30
        elif 20 <= avg_len < 40 or 120 < avg_len <= 160:
            score += 15

    consecutive_caps = len(re.findall(r"[A-Z]{4,}", cv_text))
    if consecutive_caps < 5:
        score += 20

    special_char_ratio = len(re.findall(r"[^\w\s.,;:()\-/|@+#%&'\"!?]", cv_text)) / max(len(cv_text), 1)
    if special_char_ratio < 0.02:
        score += 25

    if len(cv_text) > 100:
        score += 25

    return round(min(score, 100), 1)


def compute_overall_score(ats: float, keyword: float, format_: float) -> float:
    return round(ats * 0.4 + keyword * 0.35 + format_ * 0.25, 1)


def generate_verdict(score: float) -> str:
    if score >= 85:
        return "Excellent – Your resume is highly optimised."
    if score >= 70:
        return "Good – Minor improvements recommended."
    if score >= 50:
        return "Average – Several areas need attention."
    return "Poor – Significant improvements needed to pass ATS filters."


def generate_recommendations(
    ats: float, keyword: float, format_: float, keywords: dict, skills: list
) -> list[dict]:
    recs = []

    if ats < 60:
        recs.append({"type": "HIGH", "text": "Add clear section headers: Experience, Education, Skills, Summary."})
    if keyword < 60:
        missing = keywords.get("missing", [])[:5]
        if missing:
            recs.append({"type": "HIGH", "text": f"Include missing keywords from the job description: {', '.join(missing)}."})
    if format_ < 60:
        recs.append({"type": "MEDIUM", "text": "Improve formatting: use bullet points and avoid excessive special characters."})
    if ats < 80:
        recs.append({"type": "MEDIUM", "text": "Add contact information (email, phone) at the top of the resume."})
    if not skills:
        recs.append({"type": "HIGH", "text": "Include a dedicated Skills section with relevant technical skills."})
    partial = keywords.get("partial", [])[:3]
    if partial:
        recs.append({"type": "LOW", "text": f"Consider using exact industry terms for: {', '.join(partial)}."})
    if keyword >= 80 and ats >= 80:
        recs.append({"type": "LOW", "text": "Quantify your achievements with metrics (e.g., 'Reduced load time by 40%')."})

    return recs
