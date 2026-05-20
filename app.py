from flask import Flask, render_template, request
import os

from utils.parser import extract_text_from_pdf, clean_text, extract_skills_nlp
from utils.similarity import final_score

app = Flask(__name__)

UPLOAD_FOLDER = "resume"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        files = request.files.getlist("resumes")
        job_desc = request.form["job_desc"]

        results = []

        for file in files:
            if file:
                file_path = os.path.join(UPLOAD_FOLDER, file.filename)
                file.save(file_path)

                text = extract_text_from_pdf(file_path)
                cleaned = clean_text(text)

                resume_skills = extract_skills_nlp(cleaned)
                jd_skills = extract_skills_nlp(job_desc.lower())

                score, matched = final_score(cleaned, job_desc, resume_skills, jd_skills)

                results.append({
                    "name": file.filename,
                    "score": score,
                    "skills": matched
                })

        # Sort results
        results = sorted(results, key=lambda x: x["score"], reverse=True)

        return render_template("result.html", results=results)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)