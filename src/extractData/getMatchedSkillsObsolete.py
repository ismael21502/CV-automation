import json
import re

def normalize(skill):
    skill = skill.lower()
    skill = re.sub(r"\(.*?\)", "", skill)
    return skill.strip()

ALIASES = {
    "sql databases": "sql",
    "apis": "api",
    "rest apis": "api",
    "github": "git",
    "git/github": "git"
}

def canonical(skill):
    skill = normalize(skill)
    return ALIASES.get(skill, skill)

jobDescription = {
  "title": "Practicante de Desarrollo de Software",
  "seniority": "",
  "required_skills": [
    "JavaScript",
    "Python",
    "C#",
    "Java",
    "web development",
    "APIs",
    "SQL databases",
    "Git/GitHub",
    "Automation tools"
  ],
  "domains": [
    "Software Development",
    "Automation",
    "CRM",
    "Conversational Agents",
    "Legal Services"
  ],
  "soft_skills": [
    "analysis",
    "problem solving",
    "organization",
    "responsibility",
    "autonomy",
    "communication",
    "teamwork",
    "proactivity",
    "curiosity",
    "attention to detail",
    "openness to learning"
  ],
  "experience_years": 0
}

def getMatchedSkills(jobDescription, hardSkills):
    # Normalizar skills de la vacante una sola vez
    jobSkills = {
        canonical(skill)
        for skill in jobDescription["required_skills"]
    }
    matchedSkills = []
    for skill in hardSkills:
        mySkill = canonical(skill)
        if mySkill in jobSkills:
            matchedSkills.append(skill)
    afinityPercentage = round(len(matchedSkills)/len(jobSkills)*100)

    return afinityPercentage, matchedSkills
