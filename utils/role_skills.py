"""
Role-based skill auto-injection.
When the job description mentions a known role, the standard skills for that
role are automatically added to the JD skill set — no manual listing needed.
"""

ROLE_SKILLS = {

    # ── Finance & Accounting ─────────────────────────────────────────────────
    "finance": [
        "financial analysis", "financial modeling", "accounting", "excel",
        "investment banking", "valuation", "budgeting", "forecasting",
        "sap fico", "tally", "statistics", "data analysis",
        "power bi", "tableau", "ms office", "sql"
    ],
    "financial analyst": [
        "financial analysis", "financial modeling", "excel", "valuation",
        "budgeting", "forecasting", "statistics", "data analysis",
        "power bi", "sql", "ms office"
    ],
    "accountant": [
        "accounting", "tally", "sap fico", "ms office", "excel",
        "financial analysis", "budgeting", "taxation", "auditing"
    ],
    "investment banking": [
        "investment banking", "financial modeling", "valuation", "excel",
        "financial analysis", "statistics", "ms office", "sql"
    ],
    "risk analyst": [
        "financial analysis", "statistics", "excel", "sql",
        "data analysis", "financial modeling", "ms office"
    ],

    # ── Human Resources ───────────────────────────────────────────────────────
    "hr": [
        "recruitment", "talent acquisition", "employee engagement",
        "payroll", "communication", "leadership", "ms office",
        "negotiation", "presentation", "teamwork", "jira", "notion"
    ],
    "human resources": [
        "recruitment", "talent acquisition", "employee engagement",
        "payroll", "communication", "leadership", "ms office",
        "negotiation", "presentation"
    ],
    "recruiter": [
        "recruitment", "talent acquisition", "communication",
        "negotiation", "ms office", "jira", "linkedin", "sourcing"
    ],
    "talent acquisition": [
        "talent acquisition", "recruitment", "sourcing",
        "communication", "negotiation", "ms office"
    ],

    # ── Software Engineering ──────────────────────────────────────────────────
    "software engineer": [
        "python", "java", "javascript", "git", "github", "sql",
        "data structures", "algorithms", "problem solving", "linux",
        "docker", "agile", "scrum", "communication"
    ],
    "software developer": [
        "python", "java", "javascript", "typescript", "git", "github",
        "sql", "docker", "agile", "scrum", "problem solving"
    ],
    "backend": [
        "python", "java", "nodejs", "sql", "postgresql", "mongodb",
        "docker", "kubernetes", "aws", "git", "rest api", "linux"
    ],
    "frontend": [
        "html", "css", "javascript", "typescript", "react", "nodejs",
        "git", "figma", "responsive design", "problem solving"
    ],
    "full stack": [
        "html", "css", "javascript", "react", "nodejs", "python",
        "sql", "mongodb", "docker", "git", "aws", "rest api"
    ],
    "devops": [
        "docker", "kubernetes", "jenkins", "terraform", "aws",
        "azure", "linux", "git", "github actions", "python", "bash"
    ],
    "cloud engineer": [
        "aws", "azure", "gcp", "docker", "kubernetes", "terraform",
        "linux", "python", "networking", "security"
    ],

    # ── Data ──────────────────────────────────────────────────────────────────
    "data scientist": [
        "python", "machine learning", "deep learning", "statistics",
        "numpy", "pandas", "scikit-learn", "tensorflow", "pytorch",
        "sql", "data analysis", "tableau", "power bi", "git"
    ],
    "data analyst": [
        "sql", "excel", "python", "data analysis", "tableau",
        "power bi", "statistics", "pandas", "numpy", "ms office",
        "communication", "business analysis"
    ],
    "data engineer": [
        "python", "sql", "spark", "hadoop", "kafka", "aws",
        "docker", "airflow", "postgresql", "mongodb", "git"
    ],
    "machine learning": [
        "python", "machine learning", "deep learning", "nlp",
        "tensorflow", "pytorch", "scikit-learn", "pandas",
        "numpy", "sql", "statistics", "git"
    ],
    "ai engineer": [
        "python", "machine learning", "deep learning", "nlp",
        "llm", "transformers", "generative ai", "tensorflow",
        "pytorch", "docker", "aws", "git"
    ],
    "business analyst": [
        "business analysis", "sql", "excel", "power bi", "tableau",
        "data analysis", "communication", "jira", "agile",
        "ms office", "presentation", "statistics"
    ],

    # ── Design ────────────────────────────────────────────────────────────────
    "ui ux": [
        "figma", "canva", "adobe xd", "prototyping", "wireframing",
        "user research", "html", "css", "communication", "presentation"
    ],
    "graphic designer": [
        "figma", "canva", "adobe photoshop", "adobe illustrator",
        "creativity", "communication", "presentation"
    ],
    "product designer": [
        "figma", "prototyping", "wireframing", "user research",
        "design systems", "communication", "presentation", "canva"
    ],

    # ── Marketing ─────────────────────────────────────────────────────────────
    "marketing": [
        "digital marketing", "seo", "sem", "content marketing",
        "social media marketing", "google analytics", "canva",
        "ms office", "communication", "presentation", "excel"
    ],
    "digital marketing": [
        "digital marketing", "seo", "sem", "social media marketing",
        "google analytics", "content marketing", "canva",
        "communication", "excel"
    ],
    "content writer": [
        "content marketing", "seo", "communication", "ms office",
        "research", "presentation", "social media marketing"
    ],
    "seo": [
        "seo", "sem", "google analytics", "content marketing",
        "digital marketing", "communication", "excel"
    ],

    # ── Cybersecurity ─────────────────────────────────────────────────────────
    "cybersecurity": [
        "ethical hacking", "penetration testing", "network security",
        "cybersecurity", "wireshark", "metasploit", "linux",
        "python", "sql", "communication"
    ],
    "security engineer": [
        "network security", "cybersecurity", "penetration testing",
        "linux", "python", "aws", "docker", "communication"
    ],

    # ── Mobile ────────────────────────────────────────────────────────────────
    "mobile developer": [
        "android", "flutter", "react native", "swift", "kotlin",
        "java", "git", "sql", "firebase", "agile"
    ],
    "android developer": [
        "android", "kotlin", "java", "firebase", "sql",
        "git", "agile", "rest api"
    ],
    "ios developer": [
        "swift", "ios", "xcode", "firebase", "sql",
        "git", "agile", "rest api"
    ],

    # ── Project Management ────────────────────────────────────────────────────
    "project manager": [
        "project management", "agile", "scrum", "jira", "notion",
        "communication", "leadership", "teamwork", "ms office",
        "presentation", "negotiation", "budgeting"
    ],
    "product manager": [
        "project management", "agile", "scrum", "jira", "figma",
        "business analysis", "communication", "leadership",
        "data analysis", "presentation", "sql"
    ],
    "scrum master": [
        "scrum", "agile", "jira", "communication", "leadership",
        "project management", "teamwork", "notion"
    ],

    # ── Consulting ────────────────────────────────────────────────────────────
    "consultant": [
        "business consulting", "strategy", "market research",
        "communication", "presentation", "ms office", "excel",
        "data analysis", "negotiation", "leadership"
    ],
    "management consultant": [
        "business consulting", "strategy", "market research",
        "financial analysis", "excel", "presentation",
        "communication", "data analysis", "leadership"
    ],
}


# Keywords that map fuzzy role mentions to canonical keys
ROLE_ALIASES = {
    "finance":              "finance",
    "financial":            "finance",
    "accounting":           "accountant",
    "accountant":           "accountant",
    "investment bank":      "investment banking",
    "hr":                   "hr",
    "human resource":       "human resources",
    "recruiter":            "recruiter",
    "talent":               "talent acquisition",
    "software engineer":    "software engineer",
    "software developer":   "software developer",
    "backend":              "backend",
    "front end":            "frontend",
    "frontend":             "frontend",
    "full stack":           "full stack",
    "fullstack":            "full stack",
    "devops":               "devops",
    "cloud":                "cloud engineer",
    "data scientist":       "data scientist",
    "data science":         "data scientist",
    "data analyst":         "data analyst",
    "data analysis":        "data analyst",
    "data engineer":        "data engineer",
    "machine learning":     "machine learning",
    "ml engineer":          "machine learning",
    "ai engineer":          "ai engineer",
    "artificial intelligence": "ai engineer",
    "business analyst":     "business analyst",
    "ui ux":                "ui ux",
    "ux designer":          "ui ux",
    "ui designer":          "ui ux",
    "graphic design":       "graphic designer",
    "graphic designer":     "graphic designer",
    "product designer":     "product designer",
    "marketing":            "marketing",
    "digital marketing":    "digital marketing",
    "content writer":       "content writer",
    "seo":                  "seo",
    "cybersecurity":        "cybersecurity",
    "cyber security":       "cybersecurity",
    "security engineer":    "security engineer",
    "mobile developer":     "mobile developer",
    "android":              "android developer",
    "ios":                  "ios developer",
    "flutter":              "mobile developer",
    "project manager":      "project manager",
    "product manager":      "product manager",
    "scrum master":         "scrum master",
    "consultant":           "consultant",
    "management consultant": "management consultant",
}


def detect_role_skills(text: str) -> tuple[str | None, list[str]]:
    """
    Scan `text` for known role keywords and return:
      - detected role name (or None)
      - list of standard skills for that role (or [])
    Matches the longest alias first to avoid false short matches.
    """
    text_lower = text.lower()

    # Sort aliases longest-first so "data scientist" beats "data"
    sorted_aliases = sorted(ROLE_ALIASES.keys(), key=len, reverse=True)

    for alias in sorted_aliases:
        if alias in text_lower:
            role_key = ROLE_ALIASES[alias]
            skills = ROLE_SKILLS.get(role_key, [])
            return role_key.title(), skills

    return None, []
