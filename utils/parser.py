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
skills_db = [

    # Programming
    "python", "java", "c++", "javascript", "typescript",
    "html", "css", "react", "nodejs", "flask", "django",
    "spring boot", "php", "ruby", "golang", "kotlin",

    # Data Science / AI
    "machine learning", "deep learning", "nlp",
    "data science", "tensorflow", "pytorch",
    "scikit-learn", "pandas", "numpy", "opencv",
    "generative ai", "llm", "transformers",

    # Cloud / DevOps
    "aws", "azure", "gcp", "docker", "kubernetes",
    "jenkins", "terraform", "linux", "github actions",

    # Database
    "sql", "mysql", "postgresql", "mongodb",
    "firebase", "oracle", "sqlite",

    # Analytics
    "excel", "power bi", "tableau", "data analysis",
    "business analysis", "statistics",

    # Cybersecurity
    "ethical hacking", "penetration testing",
    "network security", "cybersecurity",
    "wireshark", "metasploit",

    # Mobile Development
    "android", "flutter", "react native", "swift",

    # Marketing
    "digital marketing", "seo", "sem", "content marketing",
    "social media marketing", "google analytics",

    # Finance
    "financial analysis", "accounting", "investment banking",
    "financial modeling", "sap fico", "tally",

    # HR
    "recruitment", "talent acquisition",
    "employee engagement", "payroll",

    # Consulting / Management
    "strategy", "market research", "business consulting",
    "project management", "agile", "scrum",

    # Soft Skills
    "communication", "leadership", "teamwork",
    "problem solving", "negotiation", "presentation",

    # Tools
    "git", "github", "jira", "notion", "figma",
    "canva", "ms office"
]


def extract_skills_nlp(text):

    text = text.lower()

    found_skills = set()

    for skill in skills_db:
        if skill.lower() in text:
            found_skills.add(skill)

    return list(found_skills)