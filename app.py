from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    send_file
)

import os
import sqlite3

from flask_session import Session

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

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

app = Flask(__name__)

app.secret_key = "supersecretkey"
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = os.path.join(os.path.dirname(os.path.abspath(__file__)), "flask_sessions")
app.config["SESSION_PERMANENT"] = False
Session(app)

# =========================
# DATABASE
# =========================

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database.db")

os.makedirs(os.path.dirname(db_path), exist_ok=True)

conn = sqlite3.connect(
    db_path,
    check_same_thread=False
)

cursor = conn.cursor()

# Users Table

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT UNIQUE,

    password TEXT
)
""")

# Resumes Table

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

            questions.extend(
                skill_questions[skill_lower]
            )

    return questions[:10]


# =========================
# LOGIN
# =========================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        )

        password = request.form.get(
            "password",
            ""
        )

        if username == "" or password == "":

            return "Username or Password Missing"

        cursor.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        )

        user = cursor.fetchone()

        if user:

            if check_password_hash(
                user[2],
                password
            ):

                session["user"] = username

                return redirect("/")

        return "Invalid Credentials"

    return render_template("login.html")


# =========================
# SIGNUP
# =========================

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        username = request.form["username"]

        password = generate_password_hash(
            request.form["password"]
        )

        try:

            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )

            conn.commit()

            return redirect("/login")

        except:

            return "Username already exists"

    return render_template("signup.html")


# =========================
# LOGOUT
# =========================

@app.route("/logout")
def logout():

    session.pop("user", None)

    return redirect("/login")


# =========================
# HOME
# =========================

@app.route("/", methods=["GET", "POST"])
def index():

    if "user" not in session:

        return redirect("/login")

    if request.method == "POST":

        job_desc = request.form["job_description"]

        files = request.files.getlist("resumes")

        results = []

        for file in files:

            if file.filename == "":

                continue

            filename = file.filename

            upload_folder = "resumes"

            os.makedirs(upload_folder, exist_ok=True)

            file_path = os.path.join(
                upload_folder,
                filename
            )

            file.save(file_path)

            text = extract_text_from_pdf(
                file_path
            )

            cleaned = clean_text(text)

            # =========================
            # SKILLS
            # =========================

            resume_skills = extract_skills_nlp(
                cleaned
            )

            jd_skills = extract_skills_nlp(
                job_desc.lower()
            )

            questions = generate_questions(
                resume_skills
            )

            score, matched = final_score(
                cleaned,
                job_desc,
                resume_skills,
                jd_skills
            )

            # =========================
            # FEEDBACK
            # =========================

            feedback = []

            if score >= 80:

                feedback.append(
                    "Excellent match for the role."
                )

            elif score >= 50:

                feedback.append(
                    "Good profile but can improve."
                )

            else:

                feedback.append(
                    "Needs more relevant skills."
                )

            important_skills = [
                "python",
                "sql",
                "machine learning",
                "flask",
                "react",
                "aws"
            ]

            for skill in important_skills:

                if skill not in resume_skills:

                    feedback.append(
                        f"Consider adding {skill} skills."
                    )

            # =========================
            # SAVE DATABASE
            # =========================

            cursor.execute("""

            INSERT INTO resumes (
                candidate_name,
                score,
                skills
            )

            VALUES (?, ?, ?)

            """, (

                filename,
                score,
                ", ".join(matched)

            ))

            conn.commit()

            # =========================
            # RESULTS
            # =========================

            results.append({

                "name": filename,

                "score": round(score, 2),

                "skills": matched,

                "suggestions": feedback,

                "questions": questions

            })

        # =========================
        # SORT RESULTS
        # =========================

        results = sorted(

            results,

            key=lambda x: x["score"],

            reverse=True
        )

        # =========================
        # DASHBOARD
        # =========================

        total_resumes = len(results)

        average_score = 0

        if total_resumes > 0:

            average_score = round(

                sum(
                    r["score"]
                    for r in results
                ) / total_resumes,

                2
            )

        top_candidate = "N/A"

        if results:

            top_candidate = results[0]["name"]

        total_skills = sum(
            len(r["skills"])
            for r in results
        )

        # =========================
        # CHARTS
        # =========================

        chart_labels = [
            r["name"]
            for r in results
        ]

        chart_scores = [
            r["score"]
            for r in results
        ]

        skill_counts = {}

        for r in results:

            for skill in r["skills"]:

                if skill in skill_counts:

                    skill_counts[skill] += 1

                else:

                    skill_counts[skill] = 1

        skill_labels = list(
            skill_counts.keys()
        )

        skill_values = list(
            skill_counts.values()
        )

        return render_template(

            "result.html",

            results=results,

            total_resumes=total_resumes,

            average_score=average_score,

            top_candidate=top_candidate,

            total_skills=total_skills,

            chart_labels=chart_labels,

            chart_scores=chart_scores,

            skill_labels=skill_labels,

            skill_values=skill_values
        )

    return render_template("index.html")


# =========================
# HISTORY
# =========================

@app.route("/history")
def history():

    if "user" not in session:

        return redirect("/login")

    conn = sqlite3.connect(db_path)

    cursor = conn.cursor()

    cursor.execute("""

    SELECT candidate_name, score, skills
    FROM resumes
    ORDER BY score DESC

    """)

    history_data = cursor.fetchall()

    conn.close()

    return render_template(
        "history.html",
        history=history_data
    )


# =========================
# PDF REPORT
# =========================

@app.route("/download-report/<candidate_name>")
def download_report(candidate_name):

    if "user" not in session:

        return redirect("/login")

    conn = sqlite3.connect(db_path)

    cursor = conn.cursor()

    cursor.execute("""

    SELECT candidate_name, score, skills
    FROM resumes
    WHERE candidate_name = ?

    """, (candidate_name,))

    data = cursor.fetchone()

    conn.close()

    if not data:

        return "Candidate Not Found"

    file_name = f"{candidate_name}_report.pdf"

    doc = SimpleDocTemplate(
        file_name
    )

    styles = getSampleStyleSheet()

    elements = []

    title = Paragraph(

        "<b>ATS Resume Report</b>",

        styles['Title']
    )

    elements.append(title)

    elements.append(
        Spacer(1, 20)
    )

    elements.append(

        Paragraph(

            f"<b>Candidate:</b> {data[0]}",

            styles['BodyText']
        )
    )

    elements.append(

        Paragraph(

            f"<b>ATS Score:</b> {data[1]}%",

            styles['BodyText']
        )
    )

    elements.append(

        Paragraph(

            f"<b>Matched Skills:</b> {data[2]}",

            styles['BodyText']
        )
    )

    elements.append(
        Spacer(1, 20)
    )

    elements.append(

        Paragraph(

            "Generated by AI ATS Screening System",

            styles['Italic']
        )
    )

    doc.build(elements)

    return send_file(
        file_name,
        as_attachment=True
    )


# =========================
# RUN
# =========================

if __name__ == "__main__":

    port = int(
        os.environ.get("PORT", 5000)
    )

    app.run(
        host="0.0.0.0",
        port=port
    )