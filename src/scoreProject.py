import re

def normalize(text):
    return text.lower().strip()

ALIASES = {
    "software development": "software-development",
    "web development": "web-development",
    "sql databases": "sql",
    "apis": "api",
    "git/github": "git",
    "automation tools": "automation"
}

def canonical(text):
    text = normalize(text)
    return ALIASES.get(text, text)

def score_project(project, job):
    score = 0
    # Tecnologías
    project_tech = {
        canonical(t)
        for t in project["technologies"]
    }
    for skill in job["required_skills"]:
        if canonical(skill) in project_tech:
            score += 10
    # Domains (pesan más)
    project_domains = {
        canonical(d)
        for d in project["domains"]
    }
    for domain in job["domains"]:
        if canonical(domain) in project_domains:
            score += 15
    # Bonus por palabras clave en facts/summary
    text = (
        project["summary"] +
        " " +
        " ".join(project["facts"])
    ).lower()
    keywords = {
        "crm": 10,
        "automation": 10,
        "api": 8,
        "business": 5,
        "workflow": 5,
        "management": 5,
        "customer": 5
    }
    for keyword, value in keywords.items():
        if keyword in text:
            score += value
    return score