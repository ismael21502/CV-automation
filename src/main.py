from softSkills import selectSoftSkills
import json 
from matchedSkills import getMatchedSkills
from callAI import callAI

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
    "automation tools"
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

with open('src/data.json', 'r', encoding='utf-8') as file:
    personalData = json.load(file)

def getSummary(relevantData):
    prompt = f"""
    You are an expert resume writer.

    Using the candidate information below, write a concise professional summary for a resume.

    Requirements:
    - Maximum 35 words.
    - Professional tone.
    - Focus on the candidate's most relevant technical skills and strengths.
    - Align the summary with the target position.
    - Do not invent experience, technologies, or achievements.
    - Do not use first person ("I", "my").
    - Return ONLY the summary text.

    Candidate data:
    {relevantData}
    """
    summary = callAI(prompt)
    print("Summary: ", summary)
    

def generateCV():
    afinity, hardSkills = getMatchedSkills(jobDescription, personalData["Hard Skills"])

    if(afinity < 40):
        print("No hay match")
        return
    else:
        print(f"{afinity}%")
    softSkills = selectSoftSkills(jobDescription["soft_skills"], personalData["Soft Skills"])
    print(softSkills, hardSkills)
    relevantData = {
        "candidate": {
            "experience_level": "Entry level",
            "hard_skills": hardSkills,
            "soft_skills": softSkills
        },
        "job": {
            "title": jobDescription["title"],
            "domains": jobDescription["domains"],
        }
    }
    # getSummary(relevantData)

generateCV()