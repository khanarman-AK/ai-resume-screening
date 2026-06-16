import math
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

MIN_SCORE = 62
MAX_SCORE = 100


def calculate_similarity(resume_text, job_desc):
    documents = [resume_text, job_desc]
    tfidf = TfidfVectorizer().fit_transform(documents)
    score = cosine_similarity(tfidf[0:1], tfidf[1:2])
    return round(float(score[0][0]) * 100, 2)


def rescale(raw):
    """Rescale a 0–100 raw score to the MIN_SCORE–100 range."""
    return MIN_SCORE + (raw / 100) * (MAX_SCORE - MIN_SCORE)


def final_score(resume_text, job_desc, resume_skills, jd_skills):

    similarity_score = calculate_similarity(resume_text, job_desc)

    matched_skills = set(resume_skills) & set(jd_skills)
    n_matched = len(matched_skills)
    total = len(jd_skills)

    # ── Smart skill score using sqrt scaling ──────────────────────────────────
    # sqrt(ratio) rewards partial matches fairly:
    #   3/15 (20%) → sqrt(0.20) = 44.7%   (not penalised harshly)
    #   5/15 (33%) → sqrt(0.33) = 57.7%   (solid match)
    #   7/15 (47%) → sqrt(0.47) = 68.6%   (strong candidate)
    #  10/15 (67%) → sqrt(0.67) = 81.9%   (very strong)
    #  15/15 (100%)→ sqrt(1.00) = 100%    (perfect)
    if total > 0:
        ratio = n_matched / total
        skill_score = math.sqrt(ratio) * 100
    else:
        skill_score = 0

    # Skills count 65%, text similarity 35%
    raw = (0.35 * similarity_score) + (0.65 * skill_score)
    scaled = rescale(raw)

    # ── Matched-skill floor ───────────────────────────────────────────────────
    # Think like a recruiter: a candidate with 5+ core skills can be trained
    # on the rest. Give them a fair baseline.
    #  0 → 62 | 1 → 65 | 2 → 68 | 3 → 72 | 4 → 75
    #  5 → 79 | 6 → 83 | 7 → 86 | 8+ capped at 88
    skill_floor = min(62 + n_matched * 3.5, 88)
    scaled = max(scaled, skill_floor)

    return round(min(scaled, 100), 2), list(matched_skills)
