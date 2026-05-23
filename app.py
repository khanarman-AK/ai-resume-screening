from flask import Flask, render_template, request, redirect, session
import os
import sqlite3

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

app = Flask(__name__)

app.secret_key = "supersecretkey"

# Upload Folder

UPLOAD_FOLDER = "resumes"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Database Path

db_path = os.path.join(
    os.environ["TEMP"],
    "database.db"
)

# Create Database Table

# Create Database Tables

conn = sqlite3.connect(db_path)

cursor = conn.cursor()

# Resume Table

cursor.execute("""

CREATE TABLE IF NOT EXISTS resumes (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    candidate_name TEXT,

    score REAL,

    skills TEXT,

    job_description TEXT

)

""")

# Users Table

cursor.execute("""

CREATE TABLE IF NOT EXISTS users (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT UNIQUE,

    email TEXT UNIQUE,

    password TEXT

)

""")

conn.commit()

conn.close()

# Signup Route

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        username = request.form["username"]

        email = request.form["email"]

        password = generate_password_hash(
            request.form["password"]
        )

        conn = sqlite3.connect(db_path)

        cursor = conn.cursor()

        cursor.execute("""

        INSERT INTO users (
            username,
            email,
            password
        )

        VALUES (?, ?, ?)

        """, (

            username,
            email,
            password

        ))

        conn.commit()

        conn.close()

        return redirect("/login")

    return render_template("signup.html")

#Login Route

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]

        password = request.form["password"]

        conn = sqlite3.connect(db_path)

        cursor = conn.cursor()

        cursor.execute("""

        SELECT * FROM users
        WHERE email = ?

        """, (email,))

        user = cursor.fetchone()

        conn.close()

        if user and check_password_hash(
            user[3],
            password
        ):

            session["user"] = user[1]

            return redirect("/")

        else:

            return "Invalid Email or Password"

    return render_template("login.html")

# Logout Route

@app.route("/logout")
def logout():

    session.pop("user", None)

    return redirect("/login")


# Home Route

@app.route("/", methods=["GET", "POST"])
def index():

    if "user" not in session:

        return redirect("/login")

    if request.method == "POST":

        job_desc = request.form["job_description"]

        files = request.files.getlist("resume")

        results = []

        for file in files:

            if file.filename.endswith(".pdf"):

                # Save File

                file_path = os.path.join(
                    UPLOAD_FOLDER,
                    file.filename
                )

                file.save(file_path)

                # Extract Text

                text = extract_text_from_pdf(file_path)

                cleaned = clean_text(text)

                # Skills

                resume_skills = extract_skills_nlp(cleaned)

                jd_skills = extract_skills_nlp(
                    job_desc.lower()
                )

                # Score

                score, matched = final_score(
                    cleaned,
                    job_desc,
                    resume_skills,
                    jd_skills
                )

                # AI Feedback

                feedback = []

                if score >= 80:

                    feedback.append(
                        "Excellent match for this role"
                    )

                elif score >= 60:

                    feedback.append(
                        "Good profile but can improve further"
                    )

                else:

                    feedback.append(
                        "Resume needs improvement"
                    )

                important_skills = [

                    "python",
                    "sql",
                    "communication",
                    "leadership",
                    "excel"

                ]

                for skill in important_skills:

                    if skill not in resume_skills:

                        feedback.append(
                            f"Consider adding {skill} skills"
                        )

                if len(resume_skills) < 5:

                    feedback.append(
                        "Add more technical skills"
                    )

                feedback.append(
                    "Add projects and internship experience"
                )

                # Save Database

                conn = sqlite3.connect(db_path)

                cursor = conn.cursor()

                cursor.execute("""

                INSERT INTO resumes (

                    candidate_name,
                    score,
                    skills,
                    job_description

                )

                VALUES (?, ?, ?, ?)

                """, (

                    file.filename,
                    score,
                    ", ".join(matched),
                    job_desc

                ))

                conn.commit()

                conn.close()

                # Store Result

                results.append({

                    "name": file.filename,

                    "score": score,

                    "skills": matched,

                    "feedback": feedback

                })

        # Sort Results

        results = sorted(
            results,
            key=lambda x: x["score"],
            reverse=True
        )

        # Dashboard

        total_resumes = len(results)

        average_score = round(

            sum(r["score"] for r in results)
            / total_resumes,

            2

        ) if total_resumes > 0 else 0

        top_candidate = (

            results[0]["name"]

            if total_resumes > 0

            else "None"

        )

        total_skills = sum(
            len(r["skills"]) for r in results
        )

        # Resume Score Chart

        chart_labels = [
            r["name"] for r in results
        ]

        chart_scores = [
            r["score"] for r in results
        ]

        # Skill Frequency Chart

        all_skills = []

        for r in results:

            all_skills.extend(r["skills"])

        skill_dict = {}

        for skill in all_skills:

            if skill in skill_dict:

                skill_dict[skill] += 1

            else:

                skill_dict[skill] = 1

        skill_labels = list(skill_dict.keys())

        skill_counts = list(skill_dict.values())

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

            skill_counts=skill_counts

        )

    return render_template("index.html")


# History Route

@app.route("/history")
def history():

    if "user" not in session:

        return redirect("/login")

    conn = sqlite3.connect(db_path)

    cursor = conn.cursor()

    cursor.execute("""

    SELECT
        candidate_name,
        score,
        skills,
        job_description

    FROM resumes

    ORDER BY id DESC

    """)

    data = cursor.fetchall()

    conn.close()

    return render_template(
        "history.html",
        data=data
    )


# Run App

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )