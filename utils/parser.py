import PyPDF2
import re
import spacy

try:
    nlp = spacy.load("en_core_web_sm")
except:
    nlp = spacy.blank("en")

# Extract text
def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

# Clean text
def clean_text(text):
    text = text.lower()
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'[^a-zA-Z ]', '', text)
    return text

# 🔥 ADD THIS HERE (new function)
def extract_skills_nlp(text):
    doc = nlp(text)

    skills_db = [
        "python", "java", "machine learning", "data science",
        "sql", "excel", "flask", "django", "html", "css"
    ]

    found_skills = set()

    for token in doc:
        if token.text.lower() in skills_db:
            found_skills.add(token.text.lower())

    return list(found_skills)