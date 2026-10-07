import json 
from pydantic import BaseModel
from extractData.callAI import askAI
from extractData.llm import softSkillsModel
class Response(BaseModel):
    skills: list[str]

def selectSoftSkills(jobSoftSkills, softSkills):
    prompt = f"""
    You are a soft-skill matching system. 
    Rules: 
    - Every returned skill MUST come exactly from the candidate's softSkills list. 
    - Match skills by meaning, not only exact wording. 
    - Only accept clear semantic matches. Do not infer specific skills from broad, unrelated, or merely associated skills. 
    - Prefer the strongest matches to explicit job requirements. 
    Job soft skills: {jobSoftSkills} 
    Candidate soft skills: {softSkills}"""
    structuredModel = softSkillsModel.with_structured_output(Response)
    result = structuredModel.invoke(prompt)
    # print("Soft skills: ", result.skills)
    return result.skills
if __name__ == "__main__":
    import time
    start = time.perf_counter()
    print(selectSoftSkills(["Comunicación abierta", "Aprendizaje continuo", "Trabajo bajo presión", "Iniciativa"], ["Problem-solving", "Proactivity", "Responsibility", "Versatility", "Curiosity", "Pragmatism"]))
    end = time.perf_counter()
    print(f"La tarea tomó {end-start:.2f}s")
