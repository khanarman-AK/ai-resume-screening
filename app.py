from flask import Flask, render_template, request
import os

from utils.parser import (
    extract_text_from_pdf,
    clean_text,
    extract_skills_nlp
)

from utils.similarity import final_score

app = Flask(__name__)

UPLOAD_FOLDER = "resumes"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        job_desc = request.form["job_description"].lower()

        files = request.files.getlist("resume")

        results = []

        for file in files:

            if file.filename != "":

                file_path = os.path.join(
                    UPLOAD_FOLDER,
                    file.filename
                )

                file.save(file_path)

                # Extract Resume Text

                text = extract_text_from_pdf(file_path)

                cleaned = clean_text(text)

                # Skill Extraction

                resume_skills = extract_skills_nlp(cleaned)

                jd_skills = extract_skills_nlp(job_desc)

                # Final Score

                score, matched = final_score(
                    cleaned,
                    job_desc,
                    resume_skills,
                    jd_skills
                )

                results.append({
                    "name": file.filename,
                    "score": score,
                    "skills": matched
                })

        # Sort Results

        results = sorted(
            results,
            key=lambda x: x["score"],
            reverse=True
        )

        # Dashboard Analytics

        total_resumes = len(results)

        average_score = round(
            sum(r["score"] for r in results) / total_resumes,
            2
        ) if total_resumes > 0 else 0

        top_candidate = (
            results[0]["name"]
            if results else "None"
        )

        total_skills = sum(
            len(r["skills"]) for r in results
        )

        # Skill Frequency Data

        skill_count = {}

        for r in results:

            for skill in r["skills"]:

                if skill in skill_count:
                    skill_count[skill] += 1

                else:
                    skill_count[skill] = 1

        # Resume Score Chart Data

        chart_labels = [
            r["name"] for r in results
        ]

        chart_scores = [
            r["score"] for r in results
        ]

        # Skill Chart Data

        skill_labels = list(skill_count.keys())

        skill_values = list(skill_count.values())

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


if __name__ == "__main__":

    port = int(
        os.environ.get("PORT", 5000)
    )

    app.run(
        host="0.0.0.0",
        port=port
    )