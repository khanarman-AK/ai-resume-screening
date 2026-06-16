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
from utils.role_skills import detect_role_skills

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

def generate_questions(skills):

    questions = []

    skill_questions = {
        "python": [
            "Explain Python decorators.",
            "What is list comprehension in Python?",
            "Difference between list and tuple?"
        ],
        "sql": [
            "What is normalization?",
            "Difference between WHERE and HAVING?",
            "Explain SQL joins."
        ],
        "flask": [
            "What is Flask?",
            "Explain Flask routing.",
            "What are templates in Flask?"
        ],
        "machine learning": [
            "Difference between supervised and unsupervised learning?",
            "What is overfitting?",
            "Explain model training."
        ],
        "javascript": [
            "Difference between var, let and const?",
            "Explain closures in JavaScript.",
            "What is DOM?"
        ],
        "react": [
            "What are React components?",
            "Explain useState hook.",
            "What is virtual DOM?"
        ],
        "aws": [
            "What is AWS EC2?",
            "Explain cloud computing.",
            "Difference between IaaS and PaaS?"
        ]
    }

    for skill in skills:
        skill_lower = skill.lower()
        if skill_lower in skill_questions:
            questions.extend(skill_questions[skill_lower])

    return questions[:10]


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

            questions = generate_questions(resume_skills)

            score, matched = final_score(
                cleaned, job_desc, resume_skills, jd_skills
            )

            feedback = []

            if score >= 88:
                feedback.append("Excellent match for the role.")
            elif score >= 74:
                feedback.append("Good profile but can improve.")
            else:
                feedback.append("Needs more relevant skills.")

            important_skills = [
                "python", "sql", "machine learning",
                "flask", "react", "aws"
            ]

            for skill in important_skills:
                if skill not in resume_skills:
                    feedback.append(f"Consider adding {skill} skills.")

            cursor.execute("""
                INSERT INTO resumes (candidate_name, score, skills)
                VALUES (?, ?, ?)
            """, (filename, score, ", ".join(matched)))

            conn.commit()

            results.append({
                "name": filename,
                "score": round(score, 2),
                "skills": matched,
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
    """, (candidate_name,))

    data = local_cursor.fetchone()
    local_conn.close()

    if not data:
        return "Candidate Not Found"

    # Floor old unrescaled scores (anything below 62 predates the rescaling feature)
    display_score = max(round(float(data[1]), 2), 62)

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
