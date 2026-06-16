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


ROLE_QUESTIONS = {
    "finance": [
        "Walk me through a DCF valuation model.",
        "How do you build a 3-statement financial model?",
        "What is EBITDA and why is it used?",
        "Explain the difference between CAPEX and OPEX.",
        "How would you assess a company's liquidity position?",
        "Describe your experience with financial forecasting and budgeting.",
        "What Excel functions do you use most for financial analysis?",
        "How do you handle discrepancies in financial statements?",
    ],
    "financial analyst": [
        "How do you approach variance analysis?",
        "Walk me through building a budget vs actuals report.",
        "What financial ratios do you consider most important?",
        "Describe a time you identified a financial risk.",
        "How do you present financial data to non-finance stakeholders?",
        "What is working capital and how do you manage it?",
    ],
    "accountant": [
        "Explain the difference between cash basis and accrual accounting.",
        "How do you handle month-end close processes?",
        "What is your experience with accounts payable/receivable?",
        "How do you ensure accuracy in financial reporting?",
        "Describe your experience with tax filings and compliance.",
        "What accounting software have you used (SAP, Tally, QuickBooks)?",
    ],
    "investment banking": [
        "Walk me through a leveraged buyout (LBO) model.",
        "How do you value a company using comparable company analysis?",
        "Explain precedent transaction analysis.",
        "What factors drive M&A deal valuations?",
        "How do you construct a pitch book?",
        "Walk me through your experience in deal structuring.",
    ],
    "hr": [
        "How do you design an end-to-end recruitment process?",
        "Describe your experience with ATS platforms.",
        "How do you handle conflicts between employees?",
        "What strategies do you use to improve employee retention?",
        "How do you ensure diversity and inclusion in hiring?",
        "Describe your experience running performance review cycles.",
        "How do you manage payroll and compliance?",
        "What metrics do you track to measure HR effectiveness?",
    ],
    "human resources": [
        "How do you design an end-to-end recruitment process?",
        "What is your approach to performance management?",
        "How do you handle employee grievances?",
        "Describe your experience with HRIS systems.",
        "How do you measure employee engagement?",
        "What are your strategies for talent retention?",
    ],
    "recruiter": [
        "What sourcing strategies do you use for passive candidates?",
        "How do you write a compelling job description?",
        "Describe your screening process for shortlisting candidates.",
        "How do you manage a high-volume hiring pipeline?",
        "What metrics do you track — time-to-fill, cost-per-hire?",
        "How do you build relationships with hiring managers?",
        "Describe a difficult role you successfully filled.",
    ],
    "talent acquisition": [
        "How do you build a talent pipeline for hard-to-fill roles?",
        "What Boolean search techniques do you use on LinkedIn?",
        "How do you measure recruiter performance?",
        "Describe your employer branding experience.",
        "How do you reduce time-to-hire without compromising quality?",
    ],
    "software engineer": [
        "Explain the difference between REST and GraphQL APIs.",
        "What SOLID principles have you applied in your projects?",
        "How do you approach code reviews?",
        "Describe your experience with CI/CD pipelines.",
        "What design patterns do you use most frequently?",
        "How do you handle system scalability challenges?",
        "Walk me through how you debug a production issue.",
        "What is your approach to writing unit tests?",
    ],
    "software developer": [
        "How do you approach breaking down a large feature into tasks?",
        "Explain the MVC design pattern.",
        "What version control workflows have you used?",
        "How do you ensure code quality in a team?",
        "Describe a challenging bug you fixed.",
        "What is your experience with Agile/Scrum?",
    ],
    "backend": [
        "How do you design a RESTful API?",
        "Explain database indexing and when to use it.",
        "What is the difference between SQL and NoSQL databases?",
        "How do you handle authentication and authorization?",
        "Describe your experience with microservices architecture.",
        "How do you optimize slow database queries?",
        "What is your approach to API rate limiting and security?",
    ],
    "frontend": [
        "Explain the virtual DOM and how React uses it.",
        "What is the difference between CSS flexbox and grid?",
        "How do you optimize a web page for performance?",
        "Describe your experience with responsive design.",
        "What is your approach to accessibility (a11y)?",
        "How do you manage state in a React application?",
        "Explain the event loop in JavaScript.",
    ],
    "full stack": [
        "How do you decide which tasks belong on frontend vs backend?",
        "Describe your experience with full-stack deployment.",
        "How do you handle CORS issues?",
        "What is your preferred tech stack and why?",
        "How do you manage environment variables across environments?",
        "Describe a full-stack project you built from scratch.",
    ],
    "devops": [
        "Explain the difference between Docker and Kubernetes.",
        "How do you design a CI/CD pipeline?",
        "What is infrastructure as code? Which tools have you used?",
        "How do you handle secrets management in production?",
        "Describe your experience with monitoring and alerting.",
        "What is a blue-green deployment?",
        "How do you handle rollbacks in a production deployment?",
    ],
    "cloud engineer": [
        "Compare AWS, Azure, and GCP services.",
        "What is the shared responsibility model in cloud security?",
        "How do you design a highly available cloud architecture?",
        "Explain auto-scaling and when to use it.",
        "What is your experience with serverless computing?",
        "How do you manage cloud costs effectively?",
    ],
    "data scientist": [
        "Explain the bias-variance tradeoff.",
        "How do you handle missing data in a dataset?",
        "What is cross-validation and why is it important?",
        "Explain the difference between precision and recall.",
        "How do you choose the right ML algorithm for a problem?",
        "Describe a data science project from data to deployment.",
        "What is your experience with feature engineering?",
        "How do you explain ML results to non-technical stakeholders?",
    ],
    "data analyst": [
        "How do you approach exploratory data analysis (EDA)?",
        "What SQL queries do you find most complex?",
        "Describe a dashboard you built and the insights it provided.",
        "How do you validate data quality?",
        "What is the difference between correlation and causation?",
        "How do you handle outliers in a dataset?",
        "Describe your experience with Power BI or Tableau.",
    ],
    "data engineer": [
        "Explain ETL vs ELT pipelines.",
        "What is data partitioning and why does it matter?",
        "How do you handle schema evolution in a data pipeline?",
        "Describe your experience with Apache Spark.",
        "What is your approach to pipeline monitoring and alerting?",
        "How do you ensure data quality at scale?",
    ],
    "machine learning": [
        "Explain the difference between bagging and boosting.",
        "How do you handle class imbalance in classification?",
        "What regularization techniques have you used?",
        "Explain attention mechanisms in transformers.",
        "How do you evaluate and compare ML models?",
        "Describe your experience deploying an ML model to production.",
        "What is your approach to hyperparameter tuning?",
    ],
    "ai engineer": [
        "Explain how large language models work at a high level.",
        "What is prompt engineering and how do you apply it?",
        "How do you evaluate generative AI outputs?",
        "Describe your experience with fine-tuning pre-trained models.",
        "What are the challenges of deploying AI in production?",
        "How do you handle AI model bias and fairness?",
    ],
    "business analyst": [
        "How do you gather and document business requirements?",
        "Describe your experience creating process flow diagrams.",
        "How do you prioritize requirements with stakeholders?",
        "What methods do you use for gap analysis?",
        "Describe a project where your analysis led to a key decision.",
        "How do you handle conflicting requirements from stakeholders?",
        "What tools do you use for data analysis and reporting?",
    ],
    "ui ux": [
        "Walk me through your design process from discovery to delivery.",
        "How do you conduct user research?",
        "Describe a usability test you ran and what you changed.",
        "How do you handle design feedback from stakeholders?",
        "What is the difference between wireframes and prototypes?",
        "How do you approach designing for accessibility?",
        "Describe your experience creating a design system.",
    ],
    "graphic designer": [
        "Describe your creative process for a brand identity project.",
        "How do you ensure consistency across design assets?",
        "What tools are you most proficient in (Figma, Illustrator, Photoshop)?",
        "How do you handle client feedback and revisions?",
        "Describe a project where you had tight deadlines.",
        "How do you stay updated on design trends?",
    ],
    "product designer": [
        "How do you balance user needs with business goals?",
        "Describe your experience working within a design system.",
        "How do you measure the success of a product design?",
        "Walk me through a product you designed from 0 to 1.",
        "How do you collaborate with engineers during implementation?",
    ],
    "marketing": [
        "How do you develop a go-to-market strategy?",
        "Describe a marketing campaign you ran and its results.",
        "How do you measure ROI on marketing initiatives?",
        "What is your experience with A/B testing?",
        "How do you identify and target the right audience?",
        "Describe your experience with content marketing and SEO.",
        "What marketing analytics tools have you used?",
    ],
    "digital marketing": [
        "How do you plan and execute a paid advertising campaign?",
        "Explain the difference between SEO and SEM.",
        "How do you measure the success of a social media campaign?",
        "What is your experience with Google Analytics and Google Ads?",
        "How do you do keyword research for SEO?",
        "Describe a digital campaign that performed above expectations.",
    ],
    "content writer": [
        "How do you research and structure long-form content?",
        "Describe your experience writing for SEO.",
        "How do you adapt your tone for different audiences?",
        "What is your process for editing and proofreading?",
        "How do you measure the performance of content you've written?",
    ],
    "cybersecurity": [
        "What is the difference between a vulnerability and a threat?",
        "Explain how a SQL injection attack works.",
        "What is the OWASP Top 10?",
        "Describe your experience with penetration testing.",
        "How do you approach a security incident response?",
        "What is zero-trust security architecture?",
        "Describe your experience with SIEM tools.",
    ],
    "project manager": [
        "How do you manage scope creep in a project?",
        "Describe your experience with Agile and Scrum ceremonies.",
        "How do you handle a project that is behind schedule?",
        "What risk management strategies do you apply?",
        "How do you communicate project status to stakeholders?",
        "Describe the most complex project you have managed.",
        "How do you resolve conflicts within a project team?",
    ],
    "product manager": [
        "How do you prioritize features in a product roadmap?",
        "Describe how you gather and validate user requirements.",
        "How do you define product success metrics?",
        "Walk me through a product launch you led.",
        "How do you work with engineering and design teams?",
        "What frameworks do you use for product prioritization (RICE, MoSCoW)?",
        "How do you handle disagreements with engineering on timelines?",
    ],
    "scrum master": [
        "How do you facilitate a productive sprint retrospective?",
        "What do you do when a team member consistently misses sprint goals?",
        "How do you remove impediments from the team?",
        "Describe a situation where you coached a team through Agile adoption.",
        "How do you handle conflicts between product owner and the team?",
    ],
    "consultant": [
        "How do you structure a problem-solving framework?",
        "Describe a time you delivered a difficult recommendation to a client.",
        "How do you quickly get up to speed in a new industry?",
        "What methods do you use for market sizing?",
        "How do you manage multiple client engagements simultaneously?",
        "Describe a project where your recommendation had measurable impact.",
    ],
    "management consultant": [
        "Walk me through how you would approach a market entry strategy.",
        "How do you build a compelling executive presentation?",
        "Describe a cost optimization project you led.",
        "How do you handle pushback on your recommendations?",
        "What frameworks do you apply to organizational change management?",
    ],
    "mobile developer": [
        "What is the difference between native and cross-platform development?",
        "How do you handle app performance optimization?",
        "Describe your experience with push notifications and background tasks.",
        "How do you approach app store submission and release management?",
        "What testing strategies do you use for mobile apps?",
    ],
    "android developer": [
        "Explain the Android activity lifecycle.",
        "What is the difference between ViewModel and LiveData?",
        "How do you handle background tasks in Android?",
        "Describe your experience with Jetpack Compose.",
        "How do you optimize an Android app for battery efficiency?",
    ],
    "ios developer": [
        "Explain the iOS view controller lifecycle.",
        "What is the difference between Swift and Objective-C?",
        "How do you manage memory in Swift using ARC?",
        "Describe your experience with SwiftUI vs UIKit.",
        "How do you handle asynchronous operations in Swift?",
    ],
}


def get_role_questions(role_key: str | None) -> list[str]:
    """Return up to 6 interview questions for the given role key."""
    if not role_key:
        return []
    key = role_key.lower()
    return ROLE_QUESTIONS.get(key, [])[:6]


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
