from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

MIN_SCORE = 62
MAX_SCORE = 100

# ── Strict floor table ────────────────────────────────────────────────────────
# Each matched skill earns a MINIMUM score. Low matches stay low.
#  0 → 62 | 1 → 63 | 2 → 65 | 3 → 67 | 4 → 70
#  5 → 74 | 6 → 78 | 7 → 82 | 8 → 84 | 9+ → 86 (capped)
SKILL_FLOORS = [62, 63, 65, 67, 70, 74, 78, 82, 84, 86]


def calculate_similarity(resume_text, job_desc):
    documents = [resume_text, job_desc]
    tfidf = TfidfVectorizer().fit_transform(documents)
    score = cosine_similarity(tfidf[0:1], tfidf[1:2])
    return round(float(score[0][0]) * 100, 2)


def rescale(raw):
    """Rescale a 0–100 raw score into the MIN_SCORE–100 range."""
    return MIN_SCORE + (raw / 100) * (MAX_SCORE - MIN_SCORE)


def final_score(resume_text, job_desc, resume_skills, jd_skills):

    similarity_score = calculate_similarity(resume_text, job_desc)

    matched_skills = set(resume_skills) & set(jd_skills)
    n_matched = len(matched_skills)
    total     = len(jd_skills)

    # ── Linear skill score (strict — no sqrt boost) ───────────────────────────
    # Candidates earn exactly what their match ratio deserves.
    #   3/15 (20%) →  20   low, stays low
    #   5/15 (33%) →  33   moderate
    #   7/15 (47%) →  47   solid
    #  10/15 (67%) →  67   strong
    #  15/15 (100%)→ 100   perfect
    skill_score = (n_matched / total * 100) if total > 0 else 0

    # 40% text similarity + 60% skill match
    raw    = (0.40 * similarity_score) + (0.60 * skill_score)
    scaled = rescale(raw)

    # ── Strict floor: don't let low-skill candidates score too high ───────────
    idx   = min(n_matched, len(SKILL_FLOORS) - 1)
    floor = SKILL_FLOORS[idx]
    scaled = max(scaled, floor)

    return round(min(scaled, 100), 2), list(matched_skills)
