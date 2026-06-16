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
    return round(MIN_SCORE + (raw / 100) * (MAX_SCORE - MIN_SCORE), 2)


def final_score(resume_text, job_desc, resume_skills, jd_skills):

    similarity_score = calculate_similarity(resume_text, job_desc)

    matched_skills = set(resume_skills) & set(jd_skills)
    n_matched = len(matched_skills)

    skill_score = (n_matched / len(jd_skills)) * 100 if jd_skills else 0

    raw = (0.5 * similarity_score) + (0.5 * skill_score)

    scaled = rescale(raw)

    # Each matched skill guarantees a rising floor:
    # 0 skills→62, 1→65, 2→68, 3→71, 4→74, 5→77, 6→80, 7→83, 8+→85 (capped)
    skill_floor = min(MIN_SCORE + n_matched * 3, 85)
    scaled = max(scaled, skill_floor)

    return round(min(scaled, 100), 2), list(matched_skills)
