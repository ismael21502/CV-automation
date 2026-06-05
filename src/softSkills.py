import json 
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

