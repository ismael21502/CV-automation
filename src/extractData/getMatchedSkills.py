from extractData.callAI import askAI
import json
from extractData.llm import hardSkillsModel
from pydantic import BaseModel

class Response(BaseModel):
    skills: list[str]

def getMatchedSkills(jobSkills: list[str], userSkills: list[str]) -> list[str]:
    # """Examples:
    #         - React → Frontend Development
    #         - HTML/CSS → Web Development
    #         - FastAPI → API Development
    #         - PostgreSQL → SQL Databases"""
    prompt = f"""You are a skill-matching system.
    Your task is to identify which skills from userSkills directly or indirectly satisfy the requirements in jobSkills.
    Rules:
    - The "skills" array must contain ONLY skills that appear in userSkills.
    - A direct match occurs when a user skill represents the same technology, tool, programming language, or concept as a job skill.
    - A related match is allowed when a specific user skill reasonably implies or covers a more general job skill.
    - Do NOT infer a specific technology from a general skill.
    - Do NOT add skills that are not present in userSkills.
    - Ignore user skills that do not sufficiently match any job skill.
    jobSkills:
    {jobSkills}
    userSkills:
    {userSkills}"""
    # prompt = promptTemplate.format(jobSkills=jobSkills, userSkills=userSkills)
    # result = json.loads(askAI("fast", prompt))["skills"]
    structuredModel = hardSkillsModel.with_structured_output(Response)
    result = structuredModel.invoke(prompt)
    # print("Skills: ", result.skills)
    return result.skills



if __name__ == "__main__":
    import time
    start = time.perf_counter()
    jobSkills = [
        "Web Development",
        "API Integration",
        "SQL Databases",
        "Git",
        "AWS"
    ]
    userSkills = [
        "Python",
        "React",
        "FastAPI",
        "PostgreSQL",
        "GitHub",
        "Docker",
        "OpenCV"
    ]
    print(getMatchedSkills(jobSkills, userSkills))
    end = time.perf_counter()
    print(f"La tarea tomó {end-start:.2f}s")
    