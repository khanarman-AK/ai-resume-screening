from flask import (
    Flask,
    render_template,
    request,
    redirect,
    send_file
)

import os
import sqlite3

from itsdangerous import URLSafeSerializer
from werkzeug.middleware.proxy_fix import ProxyFix

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from utils.parser import (
    extract_text_from_pdf,
    clean_text,
    extract_skills_nlp
)

from utils.similarity import final_score
from utils.role_skills import detect_role_skills, get_role_questions
from utils.certifications import (
    extract_certifications,
    extract_experience_years,
    score_cert_relevance
)

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

SECRET_KEY = "supersecretkey-recruitiq"

_serializer = URLSafeSerializer(SECRET_KEY)


def make_token(username):
    return _serializer.dumps(username)


def verify_token(token):
    try:
        return _serializer.loads(token)
    except Exception:
        return None


def get_current_user():
    token = request.args.get("t") or request.form.get("t")
    if token:
        return verify_token(token)
    return None


# =========================
# DATABASE
# =========================

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database.db")

conn = sqlite3.connect(
    db_path,
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS resumes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidate_name TEXT,
    score REAL,
    skills TEXT
)
""")

conn.commit()


# =========================
# QUESTION GENERATOR
# =========================

def generate_questions(resume_skills, detected_role=None):
    """
    Return interview questions tailored to the detected role.
    Falls back to skill-based questions if role is unknown.
    """
    # 1. Role-specific questions (primary source)
    role_qs = get_role_questions(detected_role)
    if role_qs:
        return role_qs[:6]

    # 2. Fallback: skill-based questions when no role detected
    skill_questions = {
        "python": [
            "Explain Python decorators and give a real-world use case.",
            "What is the difference between a list and a tuple in Python?",
            "How does Python handle memory management?",
        ],
        "sql": [
            "Explain the difference between INNER JOIN and LEFT JOIN.",
            "What is database normalization and why does it matter?",
            "How do you optimize a slow SQL query?",
        ],
        "machine learning": [
            "Explain the bias-variance tradeoff.",
            "How do you handle an imbalanced dataset?",
            "What is the difference between classification and regression?",
        ],
        "javascript": [
            "Explain closures in JavaScript with an example.",
            "What is the difference between == and === ?",
            "How does the JavaScript event loop work?",
        ],
        "react": [
            "What is the virtual DOM and how does React use it?",
            "Explain the difference between useState and useEffect.",
            "How do you manage global state in a React app?",
        ],
        "aws": [
            "What is the difference between EC2 and Lambda?",
            "How do you secure an S3 bucket?",
            "Explain VPC and its components.",
        ],
        "communication": [
            "Describe a situation where you had to persuade a stakeholder.",
            "How do you adapt your communication style for different audiences?",
        ],
        "leadership": [
            "Describe a time you led a team through a difficult challenge.",
            "How do you motivate team members who are underperforming?",
        ],
    }

    questions = []
    for skill in resume_skills:
        if skill.lower() in skill_questions:
            questions.extend(skill_questions[skill.lower()])
        if len(questions) >= 6:
            break

    return questions[:6]


# =========================
# LOGIN
# =========================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username", "")
        password = request.form.get("password", "")

        if not username or not password:
            return render_template("login.html", error="Username and password are required.")

        cursor.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        )
        user = cursor.fetchone()

        if user and check_password_hash(user[2], password):
            token = make_token(username)
            return redirect(f"/?t={token}")

        return render_template("login.html", error="Invalid username or password.")

    return render_template("login.html")


# =========================
# SIGNUP
# =========================

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            return render_template("signup.html", error="All fields are required.")

        hashed = generate_password_hash(password)

        try:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed)
            )
            conn.commit()
            token = make_token(username)
            return redirect(f"/?t={token}")

        except Exception:
            return render_template("signup.html", error="Username already exists.")

    return render_template("signup.html")


# =========================
# LOGOUT
# =========================

@app.route("/logout")
def logout():
    return redirect("/login")


# =========================
# HOME
# =========================

@app.route("/", methods=["GET", "POST"])
def index():

    user = get_current_user()
    if not user:
        return redirect("/login")

    t = request.args.get("t") or request.form.get("t", "")

    if request.method == "POST":

        job_desc = request.form.get("job_description", "")
        files = request.files.getlist("resumes")
        results = []

        # Detect role once for the whole job description
        detected_role, role_skills = detect_role_skills(job_desc)

        for file in files:

            if file.filename == "":
                continue

            filename = file.filename
            upload_folder = "resumes"
            os.makedirs(upload_folder, exist_ok=True)
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)

            text = extract_text_from_pdf(file_path)
            cleaned = clean_text(text)

            resume_skills = extract_skills_nlp(cleaned)
            jd_skills = extract_skills_nlp(job_desc.lower())

            # Merge auto-injected role skills with explicitly extracted ones
            jd_skills = list(set(jd_skills) | set(role_skills))

            # ── Certification & experience detection (on raw text) ────────────
            raw_certs = extract_certifications(text)
            certs = score_cert_relevance(raw_certs, detected_role)
            exp_years = extract_experience_years(text)

            questions = generate_questions(resume_skills, detected_role)

            score, matched = final_score(
                cleaned, job_desc, resume_skills, jd_skills
            )

            n_matched   = len(matched)
            role_label  = detected_role or "this position"
            missing     = [s for s in jd_skills if s not in matched]
            top_missing = missing[:3]
            strengths   = matched[:4]

            feedback = []

            # ── 1. Overall verdict (unique per candidate) ─────────────────────
            exp_note = f" with {exp_years} years of experience" if exp_years else ""
            if score >= 90:
                feedback.append(
                    f"Outstanding fit for {role_label}{exp_note}. "
                    f"Demonstrates strong command of {', '.join(strengths[:3]) if strengths else 'key areas'} "
                    f"— highly recommend for a first-round interview."
                )
            elif score >= 83:
                skill_str = ', '.join(strengths[:3]) if strengths else f"{n_matched} core skills"
                feedback.append(
                    f"Strong candidate for {role_label}{exp_note}. "
                    f"Solid foundation in {skill_str}. "
                    f"Any remaining gaps can be bridged quickly through on-the-job exposure."
                )
            elif score >= 74:
                skill_str = ', '.join(strengths[:2]) if strengths else "several relevant areas"
                feedback.append(
                    f"Good profile for {role_label}{exp_note}. "
                    f"Has demonstrated ability in {skill_str}. "
                    f"Would benefit from a structured onboarding plan covering missing areas."
                )
            else:
                skill_str = ', '.join(strengths[:2]) if strengths else "a few relevant areas"
                feedback.append(
                    f"Partial match for {role_label}{exp_note}. "
                    f"Shows potential in {skill_str}. "
                    f"Best suited for a junior or trainee role with a growth path."
                )

            # ── 2. Certification highlight (if certs found) ───────────────────
            if certs:
                top_certs = certs[:3]
                if len(top_certs) == 1:
                    feedback.append(
                        f"Holds {top_certs[0]} certification — adds strong credibility "
                        f"and reduces ramp-up time for the {role_label} role."
                    )
                else:
                    cert_list = ", ".join(top_certs)
                    feedback.append(
                        f"Certified in: {cert_list}. "
                        f"These credentials directly support the requirements for {role_label} "
                        f"and demonstrate a commitment to professional development."
                    )

            # ── 3. Skill-specific gap advice (unique per candidate) ────────────
            if top_missing:
                missing_str = ", ".join(top_missing)
                if n_matched >= 6:
                    feedback.append(
                        f"Nearly a complete match. The only gaps for {role_label} are: "
                        f"{missing_str}. Consider a brief assessment or a 2-week onboarding sprint."
                    )
                elif n_matched >= 3:
                    feedback.append(
                        f"To become a full match for {role_label}, this candidate should "
                        f"strengthen: {missing_str}. "
                        f"These are learnable within 4–8 weeks with focused training."
                    )
                else:
                    feedback.append(
                        f"Key areas to develop before being fully ready for {role_label}: "
                        f"{missing_str}. Recommend a structured upskilling plan."
                    )

            # ── 4. Experience-based note ──────────────────────────────────────
            if exp_years:
                if exp_years >= 5:
                    feedback.append(
                        f"{exp_years} years of experience is a strong asset for {role_label}. "
                        f"Likely to need minimal supervision and can mentor junior team members."
                    )
                elif exp_years >= 2:
                    feedback.append(
                        f"{exp_years} years of relevant experience shows a solid career trajectory. "
                        f"Candidate is past the beginner stage and ready to contribute independently."
                    )
                else:
                    feedback.append(
                        f"Early-career candidate with {exp_years} year(s) of experience. "
                        f"High potential — evaluate learning speed and attitude in the interview."
                    )

            # ── 5. Trainability note for borderline candidates ─────────────────
            if 3 <= n_matched < 7 and missing and not certs:
                feedback.append(
                    f"With {n_matched} matched skills, this candidate shows clear relevance "
                    f"to {role_label}. Test problem-solving and learning agility in the interview — "
                    f"skill gaps at this level are highly trainable."
                )

            cursor.execute("""
                INSERT INTO resumes (candidate_name, score, skills)
                VALUES (?, ?, ?)
            """, (filename, score, ", ".join(matched)))

            conn.commit()

            # Skills to display: all resume skills, annotated as matched or not
            # Fall back to resume_skills if no JD skills were detected
            display_matched = matched if matched else resume_skills
            missing_skills = [s for s in jd_skills if s not in matched][:8]

            results.append({
                "name": filename,
                "score": round(score, 2),
                "skills": display_matched,
                "missing_skills": missing_skills,
                "resume_skills": resume_skills,
                "matched_set": matched,
                "certs": certs,
                "exp_years": exp_years,
                "suggestions": feedback,
                "questions": questions
            })

        results = sorted(results, key=lambda x: x["score"], reverse=True)

        total_resumes = len(results)
        average_score = round(
            sum(r["score"] for r in results) / total_resumes, 2
        ) if total_resumes > 0 else 0

        top_candidate = results[0]["name"] if results else "N/A"
        total_skills = sum(len(r["skills"]) for r in results)

        chart_labels = [r["name"] for r in results]
        chart_scores = [r["score"] for r in results]

        skill_counts = {}
        for r in results:
            for skill in r["skills"]:
                skill_counts[skill] = skill_counts.get(skill, 0) + 1

        return render_template(
            "result.html",
            results=results,
            total_resumes=total_resumes,
            average_score=average_score,
            top_candidate=top_candidate,
            total_skills=total_skills,
            chart_labels=chart_labels,
            chart_scores=chart_scores,
            skill_labels=list(skill_counts.keys()),
            skill_values=list(skill_counts.values()),
            detected_role=detected_role,
            role_skills=role_skills,
            username=user,
            t=t
        )

    return render_template("index.html", username=user, t=t)


# =========================
# HISTORY
# =========================

@app.route("/history")
def history():

    user = get_current_user()
    if not user:
        return redirect("/login")

    t = request.args.get("t", "")

    local_conn = sqlite3.connect(db_path)
    local_cursor = local_conn.cursor()

    local_cursor.execute("""
        SELECT candidate_name, score, skills
        FROM resumes
        ORDER BY score DESC
    """)

    history_data = local_cursor.fetchall()
    local_conn.close()

    return render_template(
        "history.html",
        history=history_data,
        username=user,
        t=t
    )


# =========================
# PDF REPORT
# =========================

@app.route("/download-report/<candidate_name>")
def download_report(candidate_name):

    user = get_current_user()
    if not user:
        return redirect("/login")

    local_conn = sqlite3.connect(db_path)
    local_cursor = local_conn.cursor()

    local_cursor.execute("""
        SELECT candidate_name, score, skills
        FROM resumes
        WHERE candidate_name = ?
        ORDER BY id DESC
        LIMIT 1
    """, (candidate_name,))

    data = local_cursor.fetchone()
    local_conn.close()

    if not data:
        return "Candidate Not Found"

    display_score = round(float(data[1]), 2)

    file_name = f"{candidate_name}_report.pdf"

    doc = SimpleDocTemplate(file_name)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("<b>ATS Resume Report</b>", styles['Title']))
    elements.append(Spacer(1, 20))
    elements.append(Paragraph(f"<b>Candidate:</b> {data[0]}", styles['BodyText']))
    elements.append(Paragraph(f"<b>ATS Score:</b> {display_score}%", styles['BodyText']))
    elements.append(Paragraph(f"<b>Matched Skills:</b> {data[2]}", styles['BodyText']))
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("Generated by RecruitIQ AI Screening System", styles['Italic']))

    doc.build(elements)

    return send_file(file_name, as_attachment=True)


# =========================
# RUN
# =========================

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )
