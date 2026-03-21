import re
from difflib import SequenceMatcher


def _tokenize(text: str) -> list[str]:
    return list(set(re.findall(r"\b[a-zA-Z][\w+#.]*\b", text.lower())))


def _is_partial_match(term: str, token: str, threshold: float = 0.8) -> bool:
    ratio = SequenceMatcher(None, term, token).ratio()
    return ratio >= threshold


def match_keywords(cv_text: str, job_description: str) -> dict:
    if not job_description:
        return {"found": [], "partial": [], "missing": []}

    jd_tokens = _tokenize(job_description)
    cv_lower = cv_text.lower()
    cv_tokens = _tokenize(cv_text)

    stop_words = {
        "the", "and", "or", "in", "of", "to", "a", "an", "is", "are", "was",
        "for", "with", "on", "at", "by", "from", "that", "this", "it", "be",
        "as", "not", "we", "you", "will", "have", "has", "had", "our", "their",
        "your", "they", "he", "she", "us", "can", "do", "does", "did",
    }

    jd_keywords = [t for t in jd_tokens if t not in stop_words and len(t) > 2]

    found = []
    partial = []
    missing = []

    for kw in jd_keywords:
        pattern = r"\b" + re.escape(kw) + r"\b"
        if re.search(pattern, cv_lower):
            found.append(kw)
        else:
            partial_match = any(_is_partial_match(kw, token) for token in cv_tokens if token not in stop_words)
            if partial_match:
                partial.append(kw)
            else:
                missing.append(kw)

    return {
        "found": sorted(set(found)),
        "partial": sorted(set(partial)),
        "missing": sorted(set(missing)),
    }
