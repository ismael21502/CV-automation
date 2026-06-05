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

with open('src/data.json', 'r', encoding='utf-8') as file:
    personalData = json.load(file)

job_description = {
  "title": "Practicante de Desarrollo de Software",
  "seniority": "Intern",
  "required_skills": [
    "JavaScript",
    "Python",
    "C#",
    "Java",
    "Web Development",
    "API Development",
    "SQL Databases",
    "Git/GitHub",
    "Automation",
    "Digital Tool Integration"
  ],
  "domains": [
    "Internal Applications",
    "CRM",
    "Chatbots",
    "Process Automation"
  ],
  "languages": [
    "JavaScript",
    "Python",
    "C#",
    "Java"
  ],
  "experience_years": 0
}

print("Required:", job_description["required_skills"])

# Normalizar skills de la vacante una sola vez
job_skills = {
    canonical(skill)
    for skill in job_description["required_skills"]
}
print("SKILLS: ", job_skills)
print("\nResultados:\n")

matchedSkills = []
for skill in personalData["Hard Skills"]:
    my_skill = canonical(skill)
    if my_skill in job_skills:
        print(f"✅ Match: {skill}")
        matchedSkills.append(skill)
    else:
        print(f"❌ No match: {skill}")

print(f"Porcentaje de skills matcheadas: {round(len(matchedSkills)/len(job_skills)*100)}% ")

# matchedDesiredSkills = []

# for skill in personalData["Hard Skills"]:
#     my_skill = canonical(skill)
#     if my_skill in job_desired_skills:
#         print(f"✅ Match: {skill}")
#         matchedDesiredSkills.append(skill)
#     else:
#         print(f"❌ No match: {skill}")

# print(f"Porcentaje de skills desired matcheadas: {round(len(matchedDesiredSkills)/len(job_desired_skills)*100)}% ")
relevantData = {
    "candidate": {
    "experience_level": "Entry level",
    "hard_skills": [...],
    "soft_skills": [...]
  },
}

print("Datos para la IA")
print("Skills matcheadas: ", matchedSkills)