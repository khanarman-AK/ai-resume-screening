"""
Certification and work-experience detector.
Scans raw resume text for recognised certifications, then scores
their relevance against the detected role.
"""

import re

# ── Known certifications ──────────────────────────────────────────────────────
# Each entry: (display_name, [regex patterns to match in text])
CERTIFICATIONS = [

    # Cloud / DevOps
    ("AWS Certified",               [r"aws certif", r"amazon web services certif"]),
    ("AWS Solutions Architect",     [r"solutions architect"]),
    ("AWS Developer",               [r"aws developer"]),
    ("AWS Cloud Practitioner",      [r"cloud practitioner"]),
    ("Microsoft Azure Certified",   [r"azure certif", r"az-\d{3}"]),
    ("Google Cloud Certified",      [r"google cloud certif", r"gcp certif"]),
    ("Google Associate Cloud",      [r"associate cloud engineer"]),
    ("Kubernetes (CKA/CKAD)",       [r"\bcka\b", r"\bckad\b", r"certified kubernetes"]),
    ("Docker Certified",            [r"docker certif"]),
    ("Terraform Associate",         [r"terraform associate"]),

    # Data / AI / ML
    ("TensorFlow Developer",        [r"tensorflow (developer|certif)"]),
    ("Google Data Analytics",       [r"google data analytics"]),
    ("IBM Data Science",            [r"ibm data science"]),
    ("Cloudera Data Engineer",      [r"cloudera"]),
    ("Microsoft Power BI",          [r"power bi certif", r"pl-\d{3}"]),
    ("Tableau Desktop Specialist",  [r"tableau (desktop |certified )?specialist"]),
    ("SAS Certified",               [r"sas certif"]),
    ("Databricks Certified",        [r"databricks certif"]),

    # Finance / Accounting
    ("CFA (Chartered Financial Analyst)",   [r"\bcfa\b", r"chartered financial analyst"]),
    ("CPA (Certified Public Accountant)",   [r"\bcpa\b", r"certified public accountant"]),
    ("CMA (Certified Management Accountant)",[r"\bcma\b", r"certified management accountant"]),
    ("ACCA",                        [r"\bacca\b"]),
    ("FRM (Financial Risk Manager)",[r"\bfrm\b", r"financial risk manager"]),
    ("CFP (Certified Financial Planner)",[r"\bcfp\b", r"certified financial planner"]),
    ("Series 7 / Series 63",        [r"series 7", r"series 63"]),

    # HR
    ("SHRM-CP / SHRM-SCP",          [r"\bshrm\b"]),
    ("PHR / SPHR",                  [r"\bphr\b", r"\bsphr\b"]),
    ("HRCI Certified",              [r"\bhrci\b"]),
    ("Diploma in HRM",              [r"diploma in hr", r"diploma in human resource"]),

    # Project / Product Management
    ("PMP (Project Management Professional)", [r"\bpmp\b", r"project management professional"]),
    ("PRINCE2",                     [r"\bprince2\b", r"prince 2"]),
    ("CSM (Certified Scrum Master)", [r"\bcsm\b", r"certified scrum master"]),
    ("CSPO (Certified Scrum Product Owner)", [r"\bcspo\b"]),
    ("PMI-ACP",                     [r"\bpmi.?acp\b"]),
    ("Agile Certified Practitioner",[r"agile certif"]),
    ("Six Sigma (Green/Black Belt)", [r"six sigma", r"green belt", r"black belt"]),

    # Cybersecurity
    ("CISSP",                       [r"\bcissp\b"]),
    ("CEH (Certified Ethical Hacker)",[r"\bceh\b", r"certified ethical hacker"]),
    ("CompTIA Security+",           [r"security\+", r"comptia security"]),
    ("CompTIA Network+",            [r"network\+", r"comptia network"]),
    ("CompTIA A+",                  [r"comptia a\+", r"\bcomptia a\b"]),
    ("OSCP",                        [r"\boscp\b"]),
    ("CISM",                        [r"\bcism\b"]),

    # Networking
    ("Cisco CCNA",                  [r"\bccna\b"]),
    ("Cisco CCNP",                  [r"\bccnp\b"]),
    ("Cisco CCIE",                  [r"\bccie\b"]),

    # Marketing / Digital
    ("Google Ads Certified",        [r"google ads certif"]),
    ("Google Analytics Certified",  [r"google analytics certif"]),
    ("HubSpot Certified",           [r"hubspot certif"]),
    ("Facebook Blueprint",          [r"facebook blueprint", r"meta blueprint"]),
    ("SEMrush Certification",       [r"semrush certif"]),

    # Design
    ("Adobe Certified",             [r"adobe certif"]),
    ("Figma Certified",             [r"figma certif"]),

    # General / Soft Skills
    ("Lean Six Sigma",              [r"lean six sigma"]),
    ("ISO Certified",               [r"iso certif"]),
    ("ITIL Certified",              [r"\bitil\b"]),
]


# ── Role → relevant cert keywords ────────────────────────────────────────────
ROLE_CERT_RELEVANCE = {
    "finance":              ["cfa", "cpa", "cma", "acca", "frm", "cfp", "series"],
    "financial analyst":    ["cfa", "cpa", "cma", "frm"],
    "accountant":           ["cpa", "cma", "acca"],
    "investment banking":   ["cfa", "frm", "series 7", "series 63"],
    "hr":                   ["shrm", "phr", "sphr", "hrci"],
    "human resources":      ["shrm", "phr", "hrci"],
    "recruiter":            ["shrm", "phr"],
    "software engineer":    ["aws", "azure", "google cloud", "kubernetes", "docker"],
    "software developer":   ["aws", "azure", "docker", "kubernetes"],
    "backend":              ["aws", "azure", "docker", "cka", "ckad", "kubernetes"],
    "frontend":             ["google", "adobe", "figma"],
    "full stack":           ["aws", "azure", "docker", "kubernetes"],
    "devops":               ["aws", "azure", "kubernetes", "cka", "terraform", "docker"],
    "cloud engineer":       ["aws", "azure", "google cloud", "kubernetes", "terraform"],
    "data scientist":       ["tensorflow", "google data", "ibm data", "databricks", "sas"],
    "data analyst":         ["power bi", "tableau", "google analytics", "google data"],
    "data engineer":        ["databricks", "aws", "azure", "google cloud", "cloudera"],
    "machine learning":     ["tensorflow", "databricks", "ibm data", "google"],
    "ai engineer":          ["tensorflow", "google cloud", "aws", "ibm"],
    "business analyst":     ["pmp", "agile", "six sigma", "tableau", "power bi"],
    "cybersecurity":        ["cissp", "ceh", "oscp", "comptia", "cism"],
    "security engineer":    ["cissp", "ceh", "oscp", "comptia", "cism"],
    "project manager":      ["pmp", "prince2", "csm", "six sigma", "agile", "pmi"],
    "product manager":      ["cspo", "csm", "agile", "pmp"],
    "scrum master":         ["csm", "cspo", "pmi-acp", "agile"],
    "marketing":            ["google ads", "google analytics", "hubspot", "facebook"],
    "digital marketing":    ["google ads", "google analytics", "hubspot", "semrush"],
    "mobile developer":     ["aws", "google", "firebase"],
    "consultant":           ["pmp", "six sigma", "lean", "agile", "iso"],
}


def extract_certifications(raw_text: str) -> list[str]:
    """
    Scan raw (uncleaned) resume text for recognised certifications.
    Returns a list of display names found.
    """
    text_lower = raw_text.lower()
    found = []

    for display_name, patterns in CERTIFICATIONS:
        for pattern in patterns:
            if re.search(pattern, text_lower):
                found.append(display_name)
                break  # each cert counted once

    return found


def extract_experience_years(raw_text: str) -> int | None:
    """
    Try to detect years of work experience from text patterns like:
    '5 years of experience', '3+ years', 'experience of 7 years', etc.
    Returns the highest number found, or None.
    """
    patterns = [
        r"(\d+)\+?\s+years?\s+of\s+(work\s+)?experience",
        r"experience\s+of\s+(\d+)\+?\s+years?",
        r"(\d+)\+?\s+years?\s+experience",
    ]
    found = []
    for p in patterns:
        for m in re.finditer(p, raw_text.lower()):
            try:
                found.append(int(m.group(1)))
            except Exception:
                pass
    return max(found) if found else None


def score_cert_relevance(certs: list[str], role_key: str | None) -> list[str]:
    """
    Return certs that are relevant to the given role (appear first),
    followed by other certs. All are returned — just sorted by relevance.
    """
    if not role_key:
        return certs

    key = role_key.lower()
    keywords = ROLE_CERT_RELEVANCE.get(key, [])
    relevant, others = [], []

    for cert in certs:
        cert_lower = cert.lower()
        if any(kw in cert_lower for kw in keywords):
            relevant.append(cert)
        else:
            others.append(cert)

    return relevant + others
