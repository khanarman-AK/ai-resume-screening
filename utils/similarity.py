from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def semantic_similarity(resume_text, job_desc):
    embeddings = model.encode([resume_text, job_desc])
    score = util.cos_sim(embeddings[0], embeddings[1])
    return float(score[0][0])

def final_score(resume_text, job_desc, resume_skills, jd_skills):
    sem_score = semantic_similarity(resume_text, job_desc)

    matched_skills = set(resume_skills) & set(jd_skills)
    skill_score = len(matched_skills) / len(jd_skills) if jd_skills else 0

    final = (0.7 * sem_score) + (0.3 * skill_score)

    return round(final * 100, 2), list(matched_skills)