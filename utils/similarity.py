from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_similarity(resume_text, job_desc):
    documents = [resume_text, job_desc]

    tfidf = TfidfVectorizer().fit_transform(documents)

    score = cosine_similarity(tfidf[0:1], tfidf[1:2])

    return round(float(score[0][0]) * 100, 2)


def final_score(resume_text, job_desc, resume_skills, jd_skills):

    similarity_score = calculate_similarity(resume_text, job_desc)

    matched_skills = set(resume_skills) & set(jd_skills)

    skill_score = (len(matched_skills) / len(jd_skills)) * 100 if jd_skills else 0

    final = (0.7 * similarity_score) + (0.3 * skill_score)

    return round(final, 2), list(matched_skills)